"""
Integrate the trainlib with the Ray Tune library for hyperparameter optimization

There is a large amount of boiler plate code and complexity necessary for
hyperparameter tuning with ray tune.  This module tries to
be (sort of) minimally intrusive while taking care of most of the stuff.
Hopefully a couple days of work trying to get ray tune working is brought down
to a couple hours.

See examples/hyperparam_opt.py in the repository.
"""
import simple_parsing as sp
from functools import partial
import dataclasses as dc
from typing import Union, Dict, Any, Callable, NewType
from ray import tune
import os

from simplepytorch import logging_tools
from simplepytorch import trainlib as TL


@dc.dataclass
class ResourcesPerTrial:
    gpu:int
    cpu:int


@dc.dataclass
class RTLDefaults:
    """Default options for Ray Tune. """
    #
    #  You could integrate it into your commandline parser (using simple_parsing)

    #      >>> parser = simple_parsing.ArgumentParser()
    #      >>> parser.add_arguments(RTLCmdLine, dest='rtlargs')
    num_samples:int  # how many times to sample the hyperparameter space
    metric: str  # used by scheduler and checkpointing.  Must be a result, like "val_loss"
    mode: str = sp.choice('min', 'max')  #  whether to maximize or minimize the metric
    resources_per_trial: ResourcesPerTrial
    #  keep_checkpoints_num:int = 2

    resume:Union[bool,str] = False  # choosing --resume "ERRORED_ONLY"  picks up where left off.

    # settings you probably don't want to change

    local_dir:str = 'results/'  # where to save results
    working_directory:str = os.path.abspath('.')  # we force all trials to use the same directory so they can find the dataset.  But this assumes that different trials won't try writing the same filepaths.


def _save_checkpoint_raytune(save_checkpoint_fn, save_fp:str, cfg:'RTLTrainConfig', cur_epoch:int, save_model_architecture=True) -> None:
    """Wrap a save_checkpoint().  Ignore the save_fp path, and instead
    write to the location that Ray prefers.

    (Could instead write to our save_fp location and then symlink to Ray's
    requested directory, but Ray complains the file does not exist).
    """
    with tune.checkpoint_dir(step=cur_epoch) as checkpoint_dir:
        save_fp = f'{checkpoint_dir}/pytorch_checkpoint.pth'
        TL.save_checkpoint(
            save_fp=save_fp, cfg=cfg, cur_epoch=cur_epoch,
            save_model_architecture=save_model_architecture
        )
        #  os.symlink(save_fp, f'{checkpoint_dir}/epoch_{cur_epoch}.pth')


@dc.dataclass
class RTLTrainConfig(TL.TrainConfig):
    """
    A drop-in replacement for the TL.TrainConfig meant to work with ray tune:
        (a) gives different default logging,
        (b) modifies save_checkpoint() to ignore the requested save_fp and
            instead use a ray tune filepath, and
        (c) modifies the experiment id to include the ray tune trial id.
    """
    # You can modify any of the TL.TrainConfig options, but be careful if modifying logger_factory to log data to tune.report(...).

    # Default logging is to use ray (and implicitly therefore tensorboard)
    # You probably don't need to change it, but you could for instance also
    # save to csv with default_logging(cfg, csv=True, other_dataloggers=...)
    logger_factory: Callable[[TL.TrainConfig], logging_tools.DataLogger] = (
        lambda cfg: TL.default_logging(cfg, other_dataloggers=[
            logging_tools.LambdaLogger(lambda rowdict: tune.report(**rowdict))]))

    def __post_init__(self):
        if tune.is_session_enabled():
            self.experiment_id = f'{self.experiment_id}/{tune.get_trial_name()}'
            self.save_checkpoint = partial(_save_checkpoint_raytune, self.save_checkpoint)


HyperParamSearchSpace = NewType('HyperParamSearchSpace', Dict[str, Any])
SampledHyperParams = NewType('SampledHyperParams', Dict[str, Any])


def _ray_train(hyperparams:SampledHyperParams,
               checkpoint_dir=None, working_directory:str=None,
               get_train_config:Callable[[Dict], RTLTrainConfig]=None):
    assert get_train_config is not None, 'required kwarg'
    assert working_directory is not None, 'required kwarg'
    if working_directory:
        # note: ray changes the working directory of the file, but since the
        # dataset is in ./data/... this causes the running code to be unable to
        # find the dataset.  We change directory with critical assumption that
        # no two trials will save overlapping files into same directory. This
        # works because all simplepytorch things are designed to write into
        # results/experiment_id/ and the experiment_id is modified for each
        # trial.
        os.chdir(working_directory)
    cfg = get_train_config(hyperparams)
    if checkpoint_dir:
        TL.load_checkpoint(
            os.path.join(checkpoint_dir, 'pytorch_checkpoint.pth'), cfg)
    cfg.train(cfg)


def ray_train(experiment_id,
              rtl_args:RTLDefaults,
              space:HyperParamSearchSpace,
              get_train_config:Callable[[SampledHyperParams], RTLTrainConfig],
              **ray_tune_kwargs):
    """Call the tune.run(...) function.  This function provides some defaults
    but you can override them by passing keyword arguments"""
    # some default settings that can be overridden
    kwargs = dict(
        name=experiment_id,
        config=space,
        scheduler=tune.schedulers.ASHAScheduler(grace_period=4),
        metric=rtl_args.metric, mode=rtl_args.mode,
        num_samples=rtl_args.num_samples,
        resources_per_trial=rtl_args.resources_per_trial.__dict__,
        local_dir=rtl_args.local_dir,
        resume=rtl_args.resume,
        #  keep_checkpoints_num=rtl_args.keep_checkpoints_num,
        checkpoint_score_attr=f'{rtl_args.mode}-{rtl_args.metric}',
        reuse_actors=True,
    )
    kwargs.update(ray_tune_kwargs)
    return tune.run(
        tune.with_parameters(
            _ray_train, working_directory=rtl_args.working_directory,
            get_train_config=get_train_config),
        **kwargs)
