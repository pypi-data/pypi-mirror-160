"""
A complete setup to train pytorch models.

To create a model, you would subclass TrainConfig.  See examples/simple_example.py
in the repository.
"""
import os
import os.path
#  from tqdm import tqdm
from typing import Callable, Union, Dict, Optional, List
import contextlib
import dataclasses as dc
import numpy as np
import random
import time
import torch as T

from simplepytorch import logging_tools
from simplepytorch.result import (
    Result, SegmentationResult,
    MultiLabelBinaryClassification, MultiClassClassification)


def train(cfg: 'TrainConfig') -> None:
    """Train the model from the given configuration, with evaluation, logging,
    and checkpointing"""
    data_logger = cfg.logger_factory(cfg)
    cur_epoch = cfg.start_epoch
    if cur_epoch == 0:
        _obtain_log_save_results(
            cfg, data_logger, cur_epoch=cur_epoch, train_seconds=np.nan,
            train_result=cfg.evaluate_perf(cfg, cfg.train_loader))
        cur_epoch += 1
    # train model
    for cur_epoch in range(cur_epoch, cfg.epochs + 1):
        with timer() as seconds:
            train_result = cfg.train_one_epoch(cfg)
        _obtain_log_save_results(
            cfg, data_logger, cur_epoch=cur_epoch, train_seconds=seconds(),
            train_result=train_result)
    data_logger.close()


def _obtain_log_save_results(cfg, data_logger, cur_epoch, train_seconds, train_result):
    """Evaluate performance on val and test sets, log to disk, save model checkpoint"""
    log_data = {'epoch': cur_epoch, 'seconds_training_epoch': train_seconds}
    log_data.update(train_result.asdict('train_'))
    # get val and test performance
    if cfg.val_loader is not None:
        val_result = cfg.evaluate_perf(cfg, cfg.val_loader)
        log_data.update(val_result.asdict('val_'))
    if cfg.test_loader is not None:
        test_result = cfg.evaluate_perf(cfg, cfg.test_loader)
        log_data.update(test_result.asdict('test_'))
    # save model checkpoint
    if fp := cfg.checkpoint_if(cfg, log_data):
        cfg.save_checkpoint(save_fp=fp, cfg=cfg, cur_epoch=cur_epoch)
    # write to log
    data_logger.writerow(log_data)
    data_logger.flush()
    return log_data


def train_one_epoch(cfg: 'TrainConfig') -> Result:
    """A standard implementation for a supervised feedforward network"""
    cfg.model.train()
    result = cfg.result_factory()
    #  for minibatch in tqdm(cfg.train_loader, mininterval=1):
    for minibatch in cfg.train_loader:
        X = minibatch[0].to(cfg.device, non_blocking=True)
        y = minibatch[1].to(cfg.device, non_blocking=True)
        cfg.optimizer.zero_grad()
        yhat = cfg.model(X)
        loss = cfg.loss_fn(yhat, y, *minibatch[2:])
        loss.backward()
        cfg.optimizer.step()
        with T.no_grad():
            result.update(yhat=yhat, y=y, loss=loss)
    return result


def evaluate_perf(cfg: 'TrainConfig', loader=None, result_factory=None) -> Result:
    if loader is None:
        loader = cfg.val_loader
    cfg.model.eval()
    with T.no_grad():
        result = cfg.result_factory() if result_factory is None else result_factory()
        #  for minibatch in tqdm(loader, mininterval=1):
        for minibatch in loader:
            X = minibatch[0].to(cfg.device, non_blocking=True)
            y = minibatch[1].to(cfg.device, non_blocking=True)
            yhat = cfg.model(X)
            loss = cfg.loss_fn(yhat, y, *minibatch[2:])
            result.update(yhat=yhat, y=y, loss=loss)
    return result


def save_checkpoint(save_fp: str, cfg: 'TrainConfig', cur_epoch: int, save_model_architecture=True) -> None:
    state = {
        'random.getstate': random.getstate(),
        'np.random.get_state': np.random.get_state(),
        'torch.get_rng_state': T.get_rng_state(),
        'torch.cuda.get_rng_state': T.cuda.get_rng_state(cfg.device),

        'cur_epoch': cur_epoch,
    }
    if save_model_architecture:
        state.update({
            'model': cfg.model,
            'optimizer': cfg.optimizer
        })
    else:
        state.update({
            'model.state_dict': cfg.model.state_dict(),
            'optimizer.state_dict': cfg.optimizer.state_dict(),
        })

    os.makedirs(os.path.dirname(save_fp), exist_ok=True)
    T.save(state, save_fp)
    print("Checkpoint", save_fp)


@contextlib.contextmanager
def timer():
    """Example:
        >>> with timer() as seconds:
            do_something(...)
        >>> print('elapsed time', seconds())
    """
    _seconds = []

    class seconds():
        def __new__(self):
            return _seconds[0]
    _tic = time.perf_counter()
    yield seconds
    _toc = time.perf_counter()
    _seconds.append(_toc - _tic)


class IsNextValueMonotonic:
    def __init__(self, mode='max'):
        self.mode = mode
        if mode == 'max':
            self._best_score = float('-inf')
            self._is_better = lambda x: x > self._best_score
        elif mode == 'min':
            self._best_score = float('inf')
            self._is_better = lambda x: x < self._best_score
        else:
            raise ValueError("Input mode is either 'min' or 'max'")

    def __call__(self, metric_value) -> bool:
        if self._is_better(metric_value):
            self._best_score = metric_value
            return True
        return False

class CheckpointIf:
    """
    Return a filepath to save checkpoints if:
        a) the model is best performing so far
        b) the current epoch equals the last epoch (as defined in TrainConfig)
        c) the current epoch is one of the requested epochs to checkpoint

    If the epoch should be checkpointed and it satisfies at least two of (a)
    (b) or (c), then gracefully handle the situation by creating symlinks in
    advance of saving the filepath.

    This should be called at the end of an epoch during training.

        >>> fn = CheckpointIf('val_loss', mode='min',
                best_filename='best.pth',  # if not None, save checkpoint every time we get best loss.
                last_filename='epoch_{epoch}.pth',  # if not None, save checkpoint if the current epoch equals configured last epoch.
                )
        >>> fn(cfg, {'val_loss': 14.2})  # returns a filepath if model should be checkpointed
    """
    def __init__(self, metric: Optional[str]=None, mode:str='max',
                 at_epochs: List[int]=(), last:bool=True,
                 best_filename: Optional[str] = 'best.pth',
                 last_filename: Optional[str] = 'epoch_{epoch:04g}.pth',
                 at_epochs_filename: Optional[str] = 'epoch_{epoch:04g}.pth',
                 at_most_every_n_epochs=1
                 ):
        """
        `metric` the name of a metric that will be available in log_data
        `mode` either 'max' or 'min' to maximize or minimize the metric value
        `at_epochs` an optional list of epochs to checkpoint.
        `best_filename` the filename (not filepath) where to save the
            checkpoint for the best performing model so far
        `last_filename` the filename (not filepath) where to save the
            checkpoint for the final state of model at end of training
            (not compatible with early stopping)
        `at_epochs_filename` the filename (not filepath) where to save the
            checkpoint when the epoch is in `at_epochs`

        The filenames, respectively, can be assigned None if you don't want to
        save a checkpoint for the best or last epoch.
        """
        self.checkpoint_at_epochs = set(at_epochs)
        self.metric = metric
        self.at_epochs_filename = at_epochs_filename
        self.at_most_every_n_epochs = at_most_every_n_epochs
        self.prev_epoch = float('-inf')
        if last:
            self.last_filename = last_filename
            assert last_filename is not None
        else:
            self.last_filename = None
        if metric is None:
            self.best_filename = None
            self._is_best_score_yet = lambda _: False
        else:
            assert best_filename is not None
            self.best_filename = best_filename
            self._is_best_score_yet = IsNextValueMonotonic(mode)

    def __call__(self, cfg: 'TrainConfig', log_data: Dict) -> Optional[str]:
        """Return a filepath if a checkpoint should be saved"""
        if self.at_most_every_n_epochs + self.prev_epoch > log_data['epoch']:
            return

        is_best = self.best_filename is not None and self._is_best_score_yet(log_data[self.metric])
        is_last = self.last_filename is not None and log_data['epoch'] == cfg.epochs
        at_epoch = log_data['epoch'] in self.checkpoint_at_epochs
        best_fp = (f'{{cfg.base_dir}}/checkpoints/{self.best_filename}').format(cfg=cfg, **log_data)
        last_fp = (f'{{cfg.base_dir}}/checkpoints/{self.last_filename}').format(cfg=cfg, **log_data)
        at_epoch_fp = (f'{{cfg.base_dir}}/checkpoints/{self.at_epochs_filename}').format(cfg=cfg, **log_data)

        # evaluate all possible combinations, to correctly create symlinked checkpoint files
        if sum([is_best, is_last, at_epoch]) == 0:
            return
        self.prev_epoch = log_data['epoch']
        if sum([is_best, is_last, at_epoch]) == 3:
            self.symlink(at_epoch_fp, best_fp)
            self.symlink(at_epoch_fp, is_last)
            return at_epoch_fp
        elif sum([is_best, is_last, at_epoch]) == 2:
            if is_best and is_last:
                self.symlink(last_fp, best_fp)
                return last_fp
            elif is_best and at_epoch:
                self.symlink(at_epoch_fp, best_fp)
                return at_epoch_fp
            elif is_last and at_epoch:
                self.symlink(at_epoch_fp, last_fp)
                return at_epoch_fp
            else:
                assert False, 'code bug'
        elif is_best:
            #  os.makedirs(os.path.dirname(best_fp), exist_ok=True)
            if os.path.islink(best_fp): os.unlink(best_fp)
            return best_fp
        elif is_last:
            #  os.makedirs(os.path.dirname(last_fp), exist_ok=True)
            if os.path.islink(last_fp): os.unlink(last_fp)
            return last_fp
        elif at_epoch:
            #  os.makedirs(os.path.dirname(at_epoch_fp), exist_ok=True)
            return at_epoch_fp
        else:
            assert False, 'code bug'

    def symlink(self, a, b):
        """Create a symlink file `b` on disk that points to `a`
        Assume that `a` and `b` are both in the same parent directory.
        Example:
            >>> symlink('results/mdl/checkpoint/epoch_001.pth',
                        'results/mdl/checkpoint/best.pth')
        """
        os.makedirs(os.path.dirname(a), exist_ok=True)
        os.makedirs(os.path.dirname(b), exist_ok=True)
        if a == b:
            return
        if os.path.exists(b) or os.path.islink(b):
            os.unlink(b)
        while os.path.exists(b): pass  # waste time in case of os bugs
        os.symlink(os.path.basename(a),b)


def default_logging(cfg:'TrainConfig', console:bool=False, csv:bool=False,
                    other_dataloggers: List[logging_tools.DataLogger]=()
                    ) -> logging_tools.MultiplexedLogger:
    loggers = []
    if console:
        loggers.append(logging_tools.ConsoleLoggerTrainValTest())
    if csv:
        header = (
                ['epoch', 'seconds_training_epoch']
                + list(cfg.result_factory().asdict('train_'))
                + (list(cfg.result_factory().asdict('val_')) if cfg.val_loader is not None else [])
                + (list(cfg.result_factory().asdict('test_')) if cfg.test_loader is not None else [])
            )
        loggers.append(logging_tools.LogRotate(logging_tools.CsvLogger)(
            f'{cfg.base_dir}/perf.csv', header))
    for logger in other_dataloggers:
        loggers.append(logger)
    return logging_tools.MultiplexedLogger(*loggers)


@dc.dataclass
class TrainConfig:
    model: T.nn.Module
    optimizer: T.optim.Optimizer
    train_dset: T.utils.data.Dataset
    val_dset: Optional[T.utils.data.Dataset]
    test_dset: Optional[T.utils.data.Dataset]
    train_loader: T.utils.data.DataLoader
    val_loader: Optional[T.utils.data.DataLoader]
    test_loader: Optional[T.utils.data.DataLoader]
    loss_fn: Callable[[T.Tensor, T.Tensor], float]
    device: Union[T.device, str]
    epochs: int

    # Configure how to compute results.
    result_factory: Callable[[], Result]
    # You should make your own Result subclass.
    # ... or reference example configurations:
    #  result_factory = lambda: MultiLabelBinaryClassification(...)
    #  result_factory = lambda: MultiClassClassification(...)
    #  result_factory = lambda: SegmentationResult(
    #      classes=['tumor', 'infection', 'artifact'],
    #      model_final_layer=lambda x: (x > 0).long(),
    #      metrics=('mcc', 'loss', 'confusion_matrix'), )

    experiment_id: str = 'debugging'

    train_one_epoch: Callable[['TrainConfig'], Result] = train_one_epoch
    evaluate_perf: Callable[['TrainConfig'], Result] = evaluate_perf
    train: Callable[['TrainConfig'], None] = train

    # Configure Checkpointing, as used by the default cfg.train() function.
    #   The checkpoint function is evaluated in train() once before training
    #   starts and after every training epoch.  If it returns a filepath, save
    #   a checkpoint.
    #  By default, checkpoint before training starts and after training ends
    checkpoint_if: Callable[['TrainConfig', dict], Optional[str]] = CheckpointIf(at_epochs=[0], last=True)
    # ... other example checkpoint configurations:
    #  checkpoint_if = lambda cfg, log_data: None  # checkpointing disabled
    #  checkpoint_if = CheckpointIf(metric='val_acc', mode='max', at_epochs=[0], last=True)  # checkpoint the best model historically, the model before training, and the final epoch model
    #  checkpoint_if = CheckpointIf(at_epochs=[0, 10, 20], last=True)  # checkpoint at epochs 0, 10, 20, and the final epoch


    # Configure logging used by the cfg.train() function.  By default, log to
    # console and also to CSV.
    logger_factory: Callable[['TrainConfig'], logging_tools.DataLogger] = lambda cfg: default_logging(cfg, console=True, csv=True)
    # alternative, more customizable logger configurations below.  Note: choice of what to log depends on metrics available in result_factory.
    #  logger_factory = lambda cfg: default_logging(cfg)
    #  logger_factory = lambda cfg: logging_tools.MultiplexedLogger(cfg, console=True, other_dataloggers=[
    #      logging_tools.LogRotate(logging_tools.CsvLogger)(f'{cfg.base_dir}/perf.csv', ['epoch', 'seconds_training_epoch', 'train_loss', 'val_loss', ...]),
    #      logging_tools.LogRotate(logging_tools.HDFLogger)(f'{cfg.base_dir}/perf_tensors.h5', ['train_confusion_matrix', 'val_confusion_matrix']),
    #      logging_tools.LambdaLogger(lambda rowdict: print("hello", rowdict)),
    #  ])

    # stuff you probably don't want to configure

    # The function that actually saves a checkpoint.
    save_checkpoint: Callable[[str, 'TrainConfig', int], None] = save_checkpoint

    start_epoch: int = 0  # This value is subsequently modified after loading from a checkpoint using load_checkpoint

    @property
    def base_dir(self):
        return f'./results/{self.experiment_id}'


def load_checkpoint(fp: str, cfg: TrainConfig, load_random_state=True):
    """Update the model and optimizer in the given cfg.
    It's a mutable operation.  To make this point clear, don't return anything.
    """
    print('restoring from checkpoint', fp)
    S = T.load(fp, map_location=cfg.device)
    # random state and seeds
    if load_random_state:
        random.setstate(S['random.getstate'])
        np.random.set_state(S['np.random.get_state'])
        T.cuda.set_rng_state(S['torch.cuda.get_rng_state'].cpu(), cfg.device)
        T.random.set_rng_state(S['torch.get_rng_state'].cpu())
    # model + optimizer
    if 'model' in S:
        cfg.model = S['model']
    else:
        cfg.model.load_state_dict(S['model.state_dict'])
    cfg.model.to(cfg.device, non_blocking=True)
    if 'optimizer' in S:
        cfg.optimizer = S['optimizer']
    else:
        cfg.optimizer.load_state_dict(S['optimizer.state_dict'])
    cfg.start_epoch = S['cur_epoch']+1
