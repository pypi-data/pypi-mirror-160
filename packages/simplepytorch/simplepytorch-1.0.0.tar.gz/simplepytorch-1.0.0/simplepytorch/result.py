"""
Classes to store and analyze results.
"""

from typing import Tuple, Union, Dict, Callable
from collections import OrderedDict
import dataclasses as dc
import abc
import torch as T
from termcolor import colored
import numpy as np

from simplepytorch import metrics
from sklearn.metrics import roc_auc_score


class Result(abc.ABC):
    """
    Accumulate and analyze results, for instance over the course of one epoch.

    This is an abstract base class, meant to be subclassed.

    `metrics` should be a list of class variables that store the results.
       For example, if metrics = ['precision'], there should be a class
       variable (or property) like `self.precision`.
    `update` should compute and store results for all listed metrics
    """
    @property
    def metrics(self) -> Tuple[str]:
        raise NotImplementedError('a list of metrics available in the result')

    def update(self, yhat, y, loss) -> None:
        """Compute and store results given:
          `yhat` - model predictions
          `y` - ground truth
          `loss` - training loss

          For example, for a classifier result, this function can store
          a confusion matrix.  Metrics can evaluate the precision, recall or
          matthew's correlation coefficient from the matrix.
        """
        raise NotImplementedError()

    # don't need to modify below here

    def __str__(self):
        return ", ".join(
            f'{colored(k, "cyan", None, ["bold"])}: {v:.5f}'
            for k, v in self.asdict().items()
            if not isinstance(v, (list, np.ndarray))
        )

    def __repr__(self):
        return f'<Result:{self.__class__.__name__}>'

    def asdict(self, prefix='') -> Dict[str, any]:
        """Fetch the stored metrics, and output a (flattened) dictionary"""
        tmp = {f'{prefix}{k}': getattr(self, k.lower().replace(' ', '_'))
               for k in self.metrics}
        rv = dict(tmp)
        # flatten any results of type dict, and prepend the prefix as needed.
        for tmp_key in tmp:
            if isinstance(tmp[tmp_key], dict):
                subdct = {f'{prefix}{k}': v for k,v in rv.pop(tmp_key).items()}
                assert not set(subdct.keys()).intersection(rv), 'code error: Result has nested dictionaries with overlapping keys'
                rv.update(subdct)
        return rv


@dc.dataclass
class SegmentationResult(Result):
    """
    Assume labels are a stack of one or more binary segmentation masks and report results independently per mask.

    Aggregate results, for instance over the course of an epoch. Aggregates
    per-pixel errors into a binary confusion matrix for each class (evaluating
    how well foreground and background are separated).

    It also records:
     - a confusion matrix for each task.
     - the total loss (sum)
     - the number of pixels processed
     - the number of images processed

    From each confusion matrix, the dice, accuracy and matthew's correlation
    coefficient are extracted.

        >>> res = SegmentationResult(
          classes=['tumor', 'infection', 'artifact'],
          model_final_layer=None  # function to modify the given model predictions before computing confusion matrix.
          metrics=('mcc', 'acc', 'dice', 'loss', 'num_images', 'confusion_matrix', )  # ... or 'combined_confusion_matrix')
        )
        >>> res.update(yhat, y, loss)
        >>> res.asdict()  # a flattened dict of results.  For each dict key defined in `metrics`, get a value.  If value is itself a dict, merge (flatten) it into existing results.

        yhat and y should have shape (B,C,H,W) where C has num channels.  loss is a scalar tensor.
    """
    # adjustable parameters
    classes: Tuple[str] = ('',)  # e.g. ['tumor', 'infection', 'artifact']
    model_final_layer: Union[T.nn.Module, Callable[[T.Tensor], T.Tensor]] = None
    metrics: Tuple[str] = ('mcc', 'acc', 'dice', 'loss', 'num_images', 'confusion_matrix')  #'combined_confusion_matrix')

    # parameters you probably shouldn't adjust
    _cms: Dict[str, T.Tensor] = dc.field(init=False)
    loss: float = 0
    num_images: int = 0

    def __post_init__(self):
        self._cms = {k: T.zeros((2,2), dtype=T.float)
                     for k in self.classes}

    def update(self,
               yhat: T.Tensor,
               y: T.Tensor,
               loss: T.Tensor,
               ):
        assert len(self.classes) == yhat.shape[1] == y.shape[1]

        self.loss += loss.item()
        self.num_images += yhat.shape[0]
        # change yhat to predict class indices
        if self.model_final_layer is not None:
            yhat = self.model_final_layer(yhat)

        # update confusion matrix
        yhat = yhat.permute(0,2,3,1)
        y = y.permute(0,2,3,1)
        device = y.device
        assert len(self.classes) == y.shape[-1], 'sanity check'
        assert len(self.classes) == yhat.shape[-1], 'sanity check'
        for i,kls in enumerate(self.classes):
            self._cms[kls] = self._cms[kls].to(device, non_blocking=True) + metrics.confusion_matrix(
                yhat=yhat[...,i].reshape(-1),
                y=y[...,i].reshape(-1),
                num_classes=2)

    @property
    def dice(self) -> Dict[str,float]:
        ret = {}
        for kls in self.classes:
            cm = self._cms[kls]
            (_, fp), (fn, tp) = (cm[0,0], cm[0,1]), (cm[1,0], cm[1,1])
            ret[f'dice_{kls}'] = (2*tp / (tp+fp + tp+fn)).item()
        return ret

    @property
    def mcc(self) -> Dict[str,float]:
        return {
            f'mcc_{k}': metrics.matthews_correlation_coeff(
                self._cms[k]).cpu().item() for k in self.classes}

    @property
    def acc(self) -> Dict[str,float]:
        return {
            f'acc_{k}': metrics.accuracy(cm).item()
            for k,cm in self._cms.items()}

    @property
    def confusion_matrix(self) -> Dict[str, np.ndarray]:
        return {f'cm_{k}': self._cms[k].cpu().numpy() for k in self.classes}

    @property
    def combined_confusion_matrix(self) -> np.ndarray:
        """ Convert self.confusion_matrices into a flat matrix.  Useful for logging and simpler data storage"""
        tmp = T.cat([self._cms[k] for k in self.classes]).cpu().numpy()
        # add the class names for each confusion matrix as a column
        tmp = np.column_stack(np.repeat(self.classes, tmp.shape[0]), tmp)
        return tmp


@dc.dataclass
class ClassifierResult(Result):
    """
    Aggregate results, for instance over the course of an epoch and maintain a
    confusion matrix.

    DEPRECATED: Suggested to use this instead:  MultiLabelBinaryClassification(...)

    It computes a confusion matrix of the epoch, and also records
     - the total loss (sum)
     - the number of samples processed.

    From the confusion matrix, the accuracy and matthew's correlation
    coefficient are extracted.

        >>> res = ClassifierResult(
          num_classes=2,  # for binary classification
          model_final_layer=None,  # function to modify the given model predictions before confusion matrix.
          metrics=('mcc', 'acc', 'loss', 'num_samples', 'confusion_matrix')  # define what values are output by asdict()
        )
        >>> res.update(yhat, y, loss, minibatch_size)
        >>> res.asdict()  # Dict[str:Any]  Returns the MCC, ACC, Loss, Num Samples and Confusion Matrix.

        yhat and y each have shape (B,C) for B samples and C classes.
    """
    # params you can adjust
    num_classes: int
    model_final_layer: Union[T.nn.Module, Callable[[T.Tensor], T.Tensor]] = None
    metrics = ('mcc', 'acc', 'loss', 'num_samples', 'confusion_matrix')  # define what values are output by asdict()

    # params you probably shouldn't adjust
    _confusion_matrix: T.Tensor = dc.field(init=False)  # it is updated to tensor.
    loss: float = 0
    num_samples: int = 0

    def __post_init__(self):
        self._confusion_matrix = T.zeros(self.num_classes, self.num_classes)

    def update(self, yhat: T.Tensor, y: T.Tensor, loss: T.Tensor):
        minibatch_size = y.shape[0]
        # update loss
        self.loss += loss.item()
        self.num_samples += minibatch_size
        # change yhat (like apply softmax if necessary)
        if self.model_final_layer is not None:
            yhat = self.model_final_layer(yhat)
        # update confusion matrix
        self._confusion_matrix = self._confusion_matrix.to(y.device, non_blocking=True)
        self._confusion_matrix += metrics.confusion_matrix(yhat=yhat, y=y, num_classes=self.num_classes)
        assert np.allclose(self._confusion_matrix.sum().item(), self.num_samples), 'sanity check'

    @property
    def mcc(self) -> float:
        return metrics.matthews_correlation_coeff(self._confusion_matrix).item()

    @property
    def acc(self) -> float:
        return metrics.accuracy(self._confusion_matrix).item()
        #  return (self._confusion_matrix.trace() / self._confusion_matrix.sum()).item()

    @property
    def confusion_matrix(self) -> np.ndarray:
        return self._confusion_matrix.cpu().numpy()


class MultiClassClassification(Result):
    """A result class for Multi-Class Classification.
    Maintains a confusion matrix.

    This class is useful to to aggregate results, for instance over the course
    of an epoch.
    """
    @property
    def metrics(self):
        metrics = ('Loss', 'Num Samples', 'MCC', 'Acc', 'BAcc', 'cm', 'y', 'yhat', 'ROC_AUC')
        if self._num_classes == 2:
            metrics += ('Precision', 'Recall', 'F1', )
        return metrics

    def __init__(self, num_classes:int,
                 binarize_fn:Callable[[T.Tensor,float],T.Tensor]=None,
                 preprocess_fn:Callable[[T.Tensor],T.Tensor]=None):
        """
        Args:
            num_classes:  a list of binary outcomes predicted by the model.
            binarize_fn:  optional function or pytorch module to compute
                binarized predictions `yhat = binarize(model(x), threshold)`.  This is
                evaluated before computing the confusion matrix.
                For instance, `binarize_fn=(lambda yh, th: T.sigmoid(yh)>th)`.
        """
        self._cm = T.zeros((num_classes, num_classes))
        self._num_classes = num_classes
        self._binarize_fn = (lambda x, threshold: x) if binarize_fn is None else binarize_fn
        self._preprocess_fn =  (lambda x: x) if preprocess_fn is None else preprocess_fn
        self.loss = 0
        self.num_samples = 0
        if any(x in self.metrics for x in ['y', 'yhat', 'ROC_AUC']):
            self._ydata = []
            self._yhatdata = []

    @property
    def acc(self):
        """Accuracy"""
        return metrics.accuracy(self._cm).item()

    @property
    def bacc(self):
        """Balanced Accuracy"""
        return metrics.balanced_accuracy(self._cm).item()

    @property
    def mcc(self):
        """Matthew's Correlation Coefficient"""
        return metrics.matthews_correlation_coeff(self._cm).item()

    @property
    def f1(self):
        return metrics.f1_score(self._cm, mode='pos').item()

    @property
    def precision(self):
        return metrics.precision(self._cm, 'pos').item()

    @property
    def recall(self):
        return metrics.recall(self._cm, 'pos').item()

    @property
    def cm(self):
        """Output the binary confusion matrix"""
        return self._cm.numpy().tolist()

    @property
    def y(self):
        if len(self._ydata) == 0:
            return np.array([])
        if len(self._ydata) > 1:
            self._ydata = [T.cat(self._ydata, 0)]
        return self._ydata[0].cpu().numpy()

    @property
    def yhat(self):
        if len(self._yhatdata) == 0:
            return np.array([])
        if len(self._yhatdata) > 1:
            self._yhatdata = [T.cat(self._yhatdata, 0)]
        return self._yhatdata[0].cpu().numpy()

    @property
    def roc_auc(self):
        if self.y.shape[0] == 0:
            return 0 #np.array([])
        else:
            y_score = self.yhat
            multi_class = 'ovo' if y_score.shape[1] <= 25 else 'ovr'
            return roc_auc_score(
                y_true=self.y, y_score=y_score, multi_class=multi_class)

    def update(self, yhat, y, loss) -> None:
        """Compute and store results given:
          `yhat` - model predictions
          `y` - ground truth
          `loss` - training loss

          For example, for a classifier result, this function can store
          a confusion matrix.  Metrics can evaluate the precision, recall or
          matthew's correlation coefficient from the matrix.
        """
        self.num_samples += yhat.shape[0]
        self.loss += loss.item()
        yhat = self._preprocess_fn(yhat)
        binarized = self._binarize_fn(yhat, .5)
        if y.ndim == 2:
            assert y.shape[1] == 1, 'sanity check: y should be a scalar number per observation.'
            y = y.squeeze(1)
        assert y.shape == (yhat.shape[0], ), f'sanity check {y.shape} == {yhat.shape[0]}'
        assert y.dtype == binarized.dtype == T.long, 'sanity check'
        assert yhat.shape[1] >= y.max(), 'sanity check'
        self._cm += metrics.confusion_matrix(
            y, binarized, num_classes=self._cm.shape[0]).cpu()
        if any(x in self.metrics for x in ['y', 'yhat', 'ROC_AUC']):
            self._ydata.append(y.to('cpu', non_blocking=True))
            self._yhatdata.append(yhat.to('cpu', non_blocking=True))


class MultiLabelBinaryClassification(Result):
    """A result class for Multi-Label Binary Classification.
    Maintains one binary confusion matrix for each class and computes
    classification metrics from them.

    This class is useful to to aggregate results, for instance over the course
    of an epoch.
    """
    ALL_METRICS = ('Loss', 'Num Samples', 'MCC', 'Precision', 'Recall', 'F1', 'Acc', 'BAcc', 'cm', 'y', 'yhat', 'ROC_AUC')

    @property
    def metrics(self):
        return self._metrics

    def __init__(self, class_names:tuple,
                 binarize_fn:Callable[[T.Tensor, int],T.Tensor]=None,
                 report_avg:bool=False, metrics=ALL_METRICS, device='cpu'):
        """
        Args:
            class_names:  a list of task names identifying the binary outcomes predicted by the model.
            binarize_fn:  optional function or pytorch module to compute
                binarized predictions `yhat = binarize(model(x))`.  This is
                evaluated before computing the confusion matrix.
                For instance, `binarize_fn=(lambda yh: T.sigmoid(yh)>.5)`.
            report_avg:  If True, also compute the average of each metric
                across all classes.
            device:  Whether to compute the confusion matrix on the cpu or gpu.
                Generally, it should match the device used for y and yhat
        """
        self._metrics = metrics
        self._cms = OrderedDict((i, T.zeros((2,2), device=device)) for i in class_names)
        self._binarize_fn = (lambda x, thresh: x) if binarize_fn is None else binarize_fn
        self.loss = 0
        self.num_samples = 0
        self.report_avg = report_avg
        self.device = device
        if any(x in metrics for x in ['y', 'yhat', 'ROC_AUC']):
            self._ydata = OrderedDict((k, []) for k in class_names)
            self._yhatdata = OrderedDict((k, []) for k in class_names)

    @property
    def acc(self):
        """Accuracy"""
        return self._on_each_cm('Acc {class_name}', metrics.accuracy)

    @property
    def bacc(self):
        """Balanced Accuracy"""
        return self._on_each_cm('BAcc {class_name}', metrics.balanced_accuracy)

    @property
    def mcc(self):
        """Matthew's Correlation Coefficient"""
        return self._on_each_cm('MCC {class_name}', metrics.matthews_correlation_coeff)

    @property
    def f1(self):
        return self._on_each_cm('F1 {class_name}', lambda x: metrics.f1_score(x, mode='pos'))

    @property
    def precision(self):
        return self._on_each_cm(
            'Precision {class_name}', lambda x: metrics.precision(x, 'pos'))

    @property
    def recall(self):
        return self._on_each_cm(
            'Recall {class_name}', lambda x: metrics.recall(x, 'pos'))

    @property
    def cm(self):
        """Output the binary confusion matrices"""
        return {f'cm {class_name}': cm.cpu().numpy().tolist()
                for class_name, cm in self._cms.items()}

    @property
    def y(self):
        self._ydata = {k: [T.cat(v, 0)] if len(v) > 1 else v
                       for k, v in self._ydata.items()}
        return {f'y {class_name}': v[0].cpu().numpy() if len(v) else np.array([])
                for class_name, v in self._ydata.items()}

    @property
    def yhat(self):
        self._yhatdata = {k: [T.cat(v, 0)] if len(v) > 1 else v
                          for k, v in self._yhatdata.items()}
        return {f'yhat {class_name}': v[0].cpu().numpy() if len(v) else np.array([])
                for class_name, v in self._yhatdata.items()}

    @property
    def roc_auc(self):
        y = self.y
        yhat = self.yhat
        rv = {}
        for kls, yval, yhatval in zip(self._cms, y.values(), yhat.values()):
            key = f'ROC_AUC {kls}'
            if yval.shape[0] <= 0:
                rv[key] = 0
                continue
            try:
                rv[key] = roc_auc_score(
                    y_true=yval, y_score=yhatval, average=None)
            except ValueError:
                rv[key] = 0  # e.g. degenerate case when all classes are "0" or all are "1"
        if self.report_avg:
            rv['ROC_AUC AVG'] = sum(rv.values()) / len(rv)
        return rv

    def _on_each_cm(self, metric_name, fn):
        rv = {}
        avg = 0
        for kls, cm in self._cms.items():
            val = fn(cm).item()
            rv[metric_name.format(class_name=kls)] = val
            avg += val/len(self._cms)
        if self.report_avg:
            rv[metric_name.format(class_name='AVG')] = avg
        return rv

    def update(self, yhat, y, loss) -> None:
        """Compute and store results given:
          `yhat` - model predictions of shape (B,C) for B=batch size and C=len(class_names)
          `y` - ground truth of shape (B,C)
          `loss` - training loss

          For example, for a classifier result, this function can store
          a confusion matrix.  Metrics can evaluate the precision, recall or
          matthew's correlation coefficient from the matrix.
        """
        with T.no_grad():
            self.num_samples += yhat.shape[0]
            loss = loss.to(self.device, non_blocking=True)
            assert yhat.shape == y.shape
            assert yhat.ndim == 2 and yhat.shape[1] == len(self._cms), "sanity check: model outputs expected prediction shape"
            binarized = self._binarize_fn(yhat, .5)
            assert binarized.dtype == T.long, 'sanity check binarize fn'
            assert binarized.shape == y.shape, 'sanity check binarize fn'
            for i, (kls, cm) in enumerate(self._cms.items()):
                cm += metrics.confusion_matrix(y[:, i], binarized[:, i], num_classes=2).to(self.device, non_blocking=True)
                if 'y' in self.metrics or 'ROC_AUC' in self.metrics:
                    self._ydata[kls].append(y[:, i].to(self.device, non_blocking=True))
                if 'yhat' in self.metrics or 'ROC_AUC' in self.metrics:
                    self._yhatdata[kls].append(yhat[:, i].to(self.device, non_blocking=True))
            self.loss += loss.item()

