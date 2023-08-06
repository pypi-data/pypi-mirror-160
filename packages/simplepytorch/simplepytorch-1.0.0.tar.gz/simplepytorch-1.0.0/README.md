Configure and train PyTorch models with a lot of the
details already or partially implemented.

**DISCLAIMER:** This repo is used for my research.
New versions are not necessarily backwards compatible.  The API is
subject to change at a moment's notice.  If you happen to use it in your
research or work, make sure in your requirements.txt to pin the version
or reference the specific commit you used so you don't suffer unwanted
surprises.

Install
===

```
pip install --upgrade simplepytorch
```


Try an example
===

Download and extract DRIVE dataset to ./data/DRIVE

```
 $ ls data/DRIVE 
test  test.zip  training  training.zip
```

Run an experiment, and give it a name.
```
$ python examples/simple_example.py  --experiment_id test_experiment_1 --epochs 10

$ ls results/test_experiment_1
checkpoints  log  perf.csv
```

Look at training curves (note: demo only runs for 2 epochs)
```
simplepytorch_plot test_experiment  --mode1-subplots
```

Run demo, with (customizable) guarantees that code completes exactly once and
distributes jobs across GPUs.  (note: uses Redis database to temporarily
monitor current jobs).

```
redis-server  # must be installed to use the default example
./bin/example_experiments.sh
```

Use hyperparameter optimization with Ray Tune library.
```
pip install -U "simplepytorch[ray]"

python examples/hyperparam_opt.py  --experiment_id test_hyperband_1
```


Datasets:
==

The library provides PyTorch Dataset implementations for different datasets.

To use the pre-defined dataset classes, you must download the data and
unzip it yourself.  Consult Dataset class docstring for usage details.

```
import simplepytorch.datasets as D

dset = D.RITE(use_train_set=True)
dset[0]
```

For example, some downloaded datasets I use have the following structure:

```
 $ ls data/{arsn_qualdr,eyepacs,messidor,IDRiD_segmentation,RITE}
data/IDRiD_segmentation:
'1. Original Images'  '2. All Segmentation Groundtruths'   CC-BY-4.0.txt   LICENSE.txt

data/RITE:
AV_groundTruth.zip  introduction.txt  read_me.txt  test  training

data/arsn_qualdr:
README.md  annotations  annotations.zip  imgs1  imgs1.zip  imgs2  imgs2.zip

data/eyepacs:
README.md                 test          test.zip.003  test.zip.006  train.zip.001  train.zip.004
sample.zip                test.zip.001  test.zip.004  test.zip.007  train.zip.002  train.zip.005
sampleSubmission.csv.zip  test.zip.002  test.zip.005  train         train.zip.003  trainLabels.csv.zip

data/messidor:
Annotation_Base11.csv  Annotation_Base21.csv  Annotation_Base31.csv  Base11  Base21  Base31
Annotation_Base12.csv  Annotation_Base22.csv  Annotation_Base32.csv  Base12  Base22  Base32
Annotation_Base13.csv  Annotation_Base23.csv  Annotation_Base33.csv  Base13  Base23  Base33
Annotation_Base14.csv  Annotation_Base24.csv  Annotation_Base34.csv  Base14  Base24  Base34
```
