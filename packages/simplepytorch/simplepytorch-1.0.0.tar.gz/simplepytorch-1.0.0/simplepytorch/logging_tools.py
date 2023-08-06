from typing import List, Dict, Any, Optional
import abc
import atexit
import csv
import datetime as dt
import gzip
import logging
import pandas as pd
import pickle
import os
import os.path as osp
from termcolor import colored
from collections import OrderedDict

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class DataLoggerException(Exception):
    pass


class _LogRotate_LazyPassthrough:
    """Transparent class for handling log rotation only when a method or
    attribute from the logger is accessed"""
    def __init__(self, kls, init_data_logger_func, utcnow, *args, **kwargs):
        self.__kls = kls
        self.__args = args
        self.__kwargs = kwargs
        self.__initialized_logger_instance = None
        self.__init_data_logger_func = init_data_logger_func
        self.__utcnow = utcnow

    def __getattribute__(self, attr_name):
        P = '_LogRotate_LazyPassthrough'
        ga = object.__getattribute__
        if ga(self, f'{P}__initialized_logger_instance') is None and not attr_name.startswith('_LogRotate_LazyPassthrough'):
            args, kwargs = ga(self, f'{P}__args'), ga(self, f'{P}__kwargs')
            utcnow = ga(self, f'{P}__utcnow')
            setattr(self, f'{P}__initialized_logger_instance',
                    ga(self, f'{P}__init_data_logger_func')(utcnow, *args, **kwargs))
                    #  ga(self, f'{P}__kls')(*args, **kwargs))
        return getattr(
            ga(self,f'{P}__initialized_logger_instance'), attr_name)


class DataLogger(abc.ABC):
    """
    Abstract base class for all simplepytorch logging tools.
    For logging to a file, see the FileLogger base class.

    To use this API, define a subclass and then do:

        >>> dlog = DataLoggerChildClass(['col1', 'col2'])
        >>> dlog.writerow({'col1': 1, 'col2': 2})

        #  This also works, writing only col1 and col2 by default:
        >>> dlog.writerow({'a': 1, 'b': 2, 'col1': 3, 'col2': 4}, raise_if_extra_keys=False)
    """
    @abc.abstractmethod
    def writerow(self, rowdict: Dict[str, Any]):
        """Write a row to the file handler.  if `ignore_missing`, allow some
        values to be empty.  if raise_if_extra_keys, do not allow unrecognized keys in the dict"""
        raise NotImplementedError("subclasses should implement this")

    def flush(self):
        pass  # "subclasses could override this

    def close(self):
        pass  # "subclasses could override this


class FileLogger(DataLogger, abc.ABC):
    """
    Abstract base class for logging data to file.  The main addition over
    DataLogger is an API for the file handler, with required flush() and
    close() implementations.

    To use this API, define a subclass and then do:

        >>> dlog = FileLoggerChildClass('./results/data/experiment/perf.csv', ['col1', 'col2'])
        >>> dlog.writerow([1, 2])

        #  This also works, writing only col1 and col2 by default:
        >>> dlog.writerow({'a': 1, 'b': 2, 'col1': 3, 'col2': 4}, raise_if_extra_keys=False)
    """

    @abc.abstractmethod
    def _init_file_handler(self, log_fp, **kwargs):
        # this function expects to receive args and kwargs from __init__

        # self.fh = open(log_fp, 'w')
        raise NotImplementedError("subclasses should implement this")

    @abc.abstractmethod
    def _write_to_file_handler(self, rowdict):
        # actually write data to the file handler.

        #  self.fh.write(rowdict)
        raise NotImplementedError("subclasses should implement this")

    @abc.abstractmethod
    def flush(self):
        #  self.fh.flush()
        raise NotImplementedError("subclasses should implement this")

    @abc.abstractmethod
    def close(self):
        #  self.fh.close()
        raise NotImplementedError("subclasses should implement this")

    # below here are default FileLogger functions

    def __init__(self, log_fp: Optional[str], header: List[str], close_atexit=True, **extra_kwargs):
        self.header = header
        self._header_set = set(header)
        if log_fp is not None:
            os.makedirs(osp.dirname(osp.abspath(log_fp)), exist_ok=True)
            self._init_file_handler(log_fp, header=header, close_atexit=close_atexit, **extra_kwargs)
            log.info("FileLogger writing to file: %s" % log_fp)
        if close_atexit:
            atexit.register(self.close)

    def writerow(self, rowdict: Dict[str, Any], ignore_missing=False, raise_if_extra_keys=True):
        """Write a row to the file handler.  if `ignore_missing`, allow some
        values to be empty.  if raise_if_extra_keys, do not allow unrecognized keys in the dict"""
        rowdict = self._clean_rowdict(rowdict, ignore_missing, raise_if_extra_keys)
        self._write_to_file_handler(rowdict)

    def _clean_rowdict(self, rowdict, ignore_missing, raise_if_extra_keys):
        # convert to dict
        if not isinstance(rowdict, dict):
            rowdict = dict(zip(self.header, rowdict))
        if raise_if_extra_keys:
            ds = set(rowdict).difference(self._header_set)
            if ds: raise DataLoggerException(
                f"Tried to write row, but found extra key(s): {ds}")
        else: # filter only the relevant keys
            rowdict = {
                k: v for k, v in rowdict.items() if k in self._header_set}
        # handle missing keys
        missing_keys = self._header_set.difference(rowdict.keys())
        if not ignore_missing and len(missing_keys) != 0:
            raise DataLoggerException(
                "Tried to write row, but missing key(s): %s" % missing_keys)
        else:  # okay to ignore missing keys. set missing keys to None
            rowdict = {k: rowdict.get(k)
                       for k in self.header}
        return rowdict


class MultiplexedLogger(DataLogger):
    """
    Combine multiple loggers together.  The only restriction is that writerow api is stricter.

        >>> logger = MultiplexedLogger(
            LogRotate(CsvLogger)(f'perf.csv', ['epoch', 'seconds_training_epoch', 'train_loss', 'val_loss']),
            LogRotate(HDFLogger)(f'perf_cm.h5', ['train_confusion_matrix', 'val_confusion_matrix']))
        >>> logger.writerow({
            'epoch': 1, 'seconds_training_epoch': 3,
            'train_loss': 40.3, 'val_loss': 45.5,
            'train_confusion_matrix': np.ones((3,3)),
            'val_confusion_matrix': np.ones((3,3))})
    """
    def __init__(self, *loggers: DataLogger):
        self.loggers = loggers

    def flush(self):
        for l in self.loggers:
            l.flush()

    def close(self):
        for l in self.loggers:
            l.close()

    def writerow(self, rowdict: Dict[str, Any]):
        for l in self.loggers:
            if isinstance(l, FileLogger):
                l.writerow({x: rowdict[x] for x in l.header})
            else:
                l.writerow(rowdict)

    # for compatibility with DataLogger
    @property
    def header(self):
        hd = set()
        for l in self.loggers:
            hd.update(l.header)
        return hd


class LogRotate:
    """Store a history of any FileLogger to avoid overwriting old results

        >>> log = LogRotate(CsvLogger)(...)

    If the log filepath is "./a/b/c.csv" then it will get renamed to
    ./a/b/log/{utc_timestamp}_c.csv and a relative symlink at './a/b/c.csv'
    will point to the file.

    Lazy Initialization: Don't perform log rotate or initialize the logger
    class until an attribute or method is invoked from it.  This avoids writing
    to disk or doing rotation until the moment the file is written to.
    Even if lazy loading causes the log file to be created several minutes late,
    the start time used to define the log filename will be correct.
    """
    def __init__(self, data_logger_kls):
        self.kls = data_logger_kls

    def __call__(self, *args, **kwargs):
        utcnow = dt.datetime.utcnow().strftime('%Y%m%dT%H%M%S.%f')
        return _LogRotate_LazyPassthrough(
            self.kls, self.init_data_logger, utcnow, *args, **kwargs)

    def init_data_logger(self, utcnow, log_fp, *args, **kwargs):
        replacement_rel_path = f'log/{utcnow}_{osp.basename(log_fp)}'
        replacement_log_fp = f'{osp.dirname(osp.abspath(log_fp))}/{replacement_rel_path}'
        if osp.islink(log_fp):
            os.remove(log_fp)
        rv = self.kls(replacement_log_fp, *args, **kwargs)
        replacement_log_fp = f'log/{utcnow}_{osp.basename(log_fp)}'
        os.symlink(replacement_rel_path, log_fp)
        return rv


class CsvLogger(FileLogger):
    """Write data to a csv file.

        >>> log = CsvLogger(f'perf.csv', ['col1', 'col2'])
        >>> log.writerow([1, 3])
        >>> log.writerow({'col1': 1, 'col2': 3})
        >>> log.close()
    """
    def _init_file_handler(self, log_fp, header, **kwargs):
        if log_fp.endswith('.csv'):
            self.fh = open(log_fp, 'w')
        elif log_fp.endswith('.csv.gz'):
            self.fh = gzip.open(log_fp, 'wt')
        else:
            raise Exception("Unrecognized CsvLogger suffix: %s" % log_fp)
        self.writer = csv.DictWriter(self.fh, fieldnames=header)
        self.writer.writeheader()

    def _write_to_file_handler(self, rowdict):
        self.writer.writerow(rowdict)

    def flush(self):
        self.fh.flush()

    def close(self):
        self.fh.close()


class HDFLogger(FileLogger):
    """Write a dict where values are pandas dataframes to HDF file.

    Write:
        log = HDFLogger('test.h5', ['df1', ...], compression_level=0)
        log.writerow({"df1": pd.DataFrame({'col1': {('index1', 0): [1,2,3]}}), ...})

    Read:
        pd.HDFStore('test.h5', 'df1').keys()
    """
    def _init_file_handler(self, log_fp: str, compression_level=5, *args, **kwargs):
        self.complevel = compression_level
        assert log_fp.endswith('.h5')
        self.log_fp = osp.realpath(log_fp)
        self.fh = pd.HDFStore(log_fp, 'w', complevel=compression_level)

    def _write_to_file_handler(self, rowdict):
        for k, v in rowdict.items():
            if v is None: continue
            if not isinstance(v, pd.DataFrame):
                v = pd.DataFrame(v)
            self.fh.append(k, v)

    def flush(self):
        self.fh.flush()

    def close(self):
        self.fh.close()


class PickleLogger(FileLogger):
    def _init_file_handler(self, log_fp: str, **kwargs):
        assert log_fp.endswith('.pickle')
        self.fh = open(log_fp, 'wb')

    def _write_to_file_handler(self, rowdict):
        pickle.dump(rowdict, self.fh)

    def flush(self):
        self.fh.flush()

    def close(self):
        self.fh.close()

    @staticmethod
    def unpickler(fp):
        return unpickler(fp)

def unpickler(fp):
    """
    Example function to get data from PickleLogger
    >>> dcts = list(unpickler('data/results/test/grads.pickle'))
    """
    with open(fp, 'rb') as file_handler:
        while file_handler.peek(1):
            yield pickle.load(file_handler)


class ConsoleLoggerTrainValTest(DataLogger):
    """
    Print to stdout with colors.  By default, only print the values that are
    float, int, str or list values, and that are in the (optionally supplied) header.

    Fairly specific expectation on the header (it is written to work with
    simplepytorch.trainlib). Not required, but the header should contain values matching:
        {'epoch': int, 'seconds_training_epoch': float',
         'train_*': any, 'val_*': any, 'test_*': any}

    Note: if this makes it into a log file, you can view the log in color with
    bash command `less -R`.
    """
    def __init__(self, header:Optional[List[str]]=None,
                 printable_types=(int, float, str, list), ):
        """
        Args:
            header:  Optional list of columns to print to stdout.  By default, print anything.
            printable_types:  List of data types that are printable.  Only
                    print int, float, str and list types by default.
        """
        self.printable_types = printable_types
        if header is None:
            self.headers = None
        else:
            self.headers = self.get_headers(header)

    def get_headers(self, header):
        hd = {
            'train': OrderedDict([(x,None) for x in header if x.startswith('train')]),
            'val': OrderedDict([(x,None) for x in header if x.startswith('val')]),
            'test': OrderedDict([(x,None) for x in header if x.startswith('test')]),
        }
        toprow = OrderedDict([(x,None) for x in header
                              if all(x not in y for y in hd.values())])
        return OrderedDict({
            ('toprow', None): toprow,
            ('train', 'green'): hd['train'],
            ('val', 'yellow'): hd['val'],
            ('test', 'red'): hd['test'],})

    def writerow(self, rowdict:Dict[str, Any]):
        msg = self.create_msg(rowdict)
        print(msg)

    def create_msg(self, rowdict: Dict[str, Any]):
        if self.headers is None:
            headers = self.get_headers(rowdict.keys())
        else:
            headers = self.headers
        console_msg = []
        for (spec, color), field_names in headers.items():
            #  if spec == 'toprow':
                #  console_msg.append(
                    #  '{k}: {v}'.format(
                        #  k=colored(k, "cyan", None, ["bold"]),
                        #  v=self.format_value(rowdict[k])))
                #  console_msg = [', '.join(console_msg)]
            #  else:
            if color is not None and len(field_names):
                console_msg.append(
                    f'\n\t{colored(f"{spec.upper()} RESULTS: ", color, None, ["bold"])}',
                )
            console_msg.append(', '.join([
                '{k}: {v}'.format(
                    k=colored(k, "cyan", None, ["bold"]),
                    v=self.format_value(rowdict[k]))
                for k in field_names
                if isinstance(rowdict[k], self.printable_types)
                ]))
        return ''.join(console_msg)

    def format_value(self, value):
        if isinstance(value, (int, )):
            return f'{value: 4d}'
        elif isinstance(value, (float, )):
            return f'{value: .06g}'
        else:
            return value


class DoNothingLogger(DataLogger):
    def __init__(self, *args, **kwargs):
        pass

    def writerow(self, rowdict):
        pass


class LambdaLogger(DataLogger):
    """Convenience to run arbitrary code in logger without creating a class for it."""
    def __init__(self, fn):
        self.fn = fn
    def writerow(self, rowdict):
        self.fn(rowdict)

if __name__ == "__main__":
    # for manual TESTING

    logger = DoNothingLogger()
    logger.writerow()
    logger = MultiplexedLogger()
    logger.writerow({})

    print('console logger')
    logger = ConsoleLoggerTrainValTest()
    logger.writerow({'col1': 1, 'col2': 'col2', 'col3': [1,2,3]})
    logger.writerow({'epoch': 1, 'train_col1': 1, 'val_col2': 'col2', 'test_col3': [1,2,3]})
    logger.writerow({'epoch': 1, 'train_col1': 1.222222, 'val_col2': float('inf'), })

    print('multiplexed logger')
    logger = MultiplexedLogger(
        LogRotate(CsvLogger)('perf.csv', ['epoch', 'seconds_training_epoch', 'train_loss', 'val_loss']),
        LogRotate(HDFLogger)('perf_cm.h5', ['train_confusion_matrix', 'val_confusion_matrix']))
    logger.writerow({
        'epoch': 1, 'seconds_training_epoch': 3,
        'train_loss': 40.3, 'val_loss': 45.5,
        'train_confusion_matrix': pd.DataFrame({'a': [1,2,3], 'b': [1,1,1]}),
        'val_confusion_matrix': pd.DataFrame({'a': [1,1,1], 'b': [1,1,1]}),})
    logger.writerow({
        'epoch': 1, 'seconds_training_epoch': 3,
        'train_loss': 40.3, 'val_loss': 45.5,
        'train_confusion_matrix': pd.DataFrame({'a': [1,2,3], 'b': [2,2,2]}),
        'val_confusion_matrix': pd.DataFrame({'a': [2,2,2], 'b': [2,2,2]}),})
    logger.close()
    z = pd.HDFStore('perf_cm.h5')
    assert z['train_confusion_matrix'].shape == (6,2)
    assert len(set(z.keys())) == 2
    z.close()

    print('csv logger')
    a = CsvLogger('a.csv.gz', ['a', 'b'])
    b = CsvLogger('b.csv', ['a', 'b'])
    for x in [a, b]:
        x.writerow({'a': 1, 'b': 2})
        x.writerow([1, 2])
    # optional close, since done atexit by default
    a.close()
    #
    # check results on cmdline
    # zcat a.csv.gz
    # cat b.csv

    print('pickle logger')
    c = PickleLogger('c.pickle', ['a', 'b'])
    for x in [c]:
        x.writerow({'a': 1, 'b': 2})
        x.writerow([3, 4])
    # optional close, since done atexit by default
    c.close()
    #
    _h = open('c.pickle', 'rb')
    print(pickle.load(_h))
    print(pickle.load(_h))

    print('HDFLogger')
    logger = LogRotate(HDFLogger)('perf_cm2.h5', ['train_confusion_matrix', 'val_confusion_matrix'])
    logger.writerow({
        'train_confusion_matrix': pd.DataFrame({'a': [1,2,3], 'b': [1,1,1]}),
        'val_confusion_matrix': pd.DataFrame({'a': [1,1,1], 'b': [1,1,1]}),})
    logger.writerow({
        'train_confusion_matrix': pd.DataFrame({'a': [1,2,3], 'b': [2,2,2]}),
        'val_confusion_matrix': pd.DataFrame({'a': [2,2,2], 'b': [2,2,2]}),})
    logger.close()
    z = pd.HDFStore('perf_cm2.h5')
    assert z['train_confusion_matrix'].shape == (6,2)
    assert len(set(z.keys())) == 2
    print('HDF Store has', z.keys())
    print('train confusion matrix\n', z['train_confusion_matrix'].shape)
    z.close()
