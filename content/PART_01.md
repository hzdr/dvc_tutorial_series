# Exploring DVC for machine learning pipelines in research (Part 1)



This is part 1/n of my dvc tutorial series. (ongoing work in progress)
During the past months part of my job became looking at different tools to manage machine learning workflows for our team at HelmholtzAI. A lot of material accumulated on the way, thus I decided to share some of the process and what I’ve learned.
The idea is to share the comparison process itself, but also hands-on tutorials around specific tools. I’ll start with the latter as it can be read independently and the general evaluation is still ongoing.

Let’s start with exploring DVC, which turned out to become oneof our final candidates.

> DVC (Data Version Control) is basically version control expanded to the use-cases of machine learning (and similar pipelines)

We’ll dive in with a tutorial which tackles different aspects important to evaluate the suitability of the framework. After exploring the basics I hope to be able to share a real life example + application.
You can find the code on our GitHub and follow along. :)
I decided to share my general approach and why the tutorial is designed the way it is — if you are only interested in the code, feel free to jump right to the section **DVC TUTORIAL**.

### Usecase

An important aspect of choosing tools is always to have your use-case in mind. I currently work at a research facility, so our use case includes large scientific datasets, custom infrastructure (own datacenters, HPC) and a particular need for reproducibility. 
Based on this, the boxes a tool must tick, are:

- Reproducibility: Verifiable results are crucial for research. If the results were obtained by using ML anywhere along the way, this part must also be reproducible for independent researchers. A typical ML project contains code, (several) datasets, various parameters, (several) models, further different experiments and so forth..

- Workflow integration: As the tool might be used both by IT professionals and scientists, thus it needs to be as non-invasive as possible — you can’t expect a scientist with some basic coding skills to detangle framework specific code from ML code.

- Exchangeable backend: We have our own datacenters and cloud infrastructure, thus the tooling must be able to work with custom storage solutions.

- Framework agnostic: It shouldn’t care if we use pytorch, tensorflow or a custom library. If it’s also language agnostic, this would be preferred.

- Open source: We think it’s the right thing to do and support. Also, usually it’s much easier to adapt to custom needs.

- Other: We prefer solutions that we can tweak towards our needs. Also, budget matters.


### Tutorial setup

When testing multiple frameworks against each other, there is need for a common base. The example should be consistent across test scenarios and adjusted where necessary — every tool integrates differently into the code. Here is a rough setup of the idea:

```
Pipeline: 
- integrate $tool into workflow
- run ml-pipeline with $tool
Parameters:
Test logging, altering and retrieving:
- parameter 1 (val0, val1, val2)
- parameter 2 (val0, val1, val2)
Metrics:
Test logging, exchanging and retrieving:
- metric 1 .. metric n
Models:
Test exchangeability of models
- model 1 (type, parameters, metrics)
- model 2 (type, parameters, metrics)
Dataset:
Storing, altering, versioning and retrieving
- small dataset (PoC)
- large dataset
```

## The example
In order to use something (relatively) official and well tested, I decided to utilize an [example](!https://www.mlflow.org/docs/latest/tutorials-and-examples/tutorial.html) found in the tutorials section of another tool, [MLflow](!https://mlflow.org/) which is also one of our hot candidates.
It turned out that the example needed some closer examination and adjustments. As its always interesting to understand what one is working with, you can find some additional information about the example itself [here](!https://github.com/hzdr/dvc_tutorial_series/blob/master/content/EXAMPLE.md).


Let's get to work!

## DVC TUTORIAL

I currently use OSX and manage my environments with [conda](!https://docs.conda.io/en/latest/). 
You can find a very basic `environment.yml` in the repository, which lists additional packages you’ll need.
Make sure to [have DVC installed](!https://dvc.org/doc/install) within your working environment before you start.

Sometimes I’ll add a commands output for better comprehension within the command block.


### Preparation:

Go to a project directory of your choice and clone the repository:

`git clone git@github.com:hzdr/dvc_tutorial_series.git`

Switch into the source directory and initialize git and dvc:
```
cd dvc_tutorial_series/src
git init
dvc init
```

Add the remote storage to use (we will stay on our local machine in this case):
```
mkdir /tmp/dvc_demo_test
dvc remote add -d localremote /tmp/dvc_demo_test
dvc remote list
```

>DVC stores information about the added data in a special file named wine-quality.csv.dvc, a small text file with a human-readable format. 
We can version this file like source code with Git, as a placeholder for the original data (which gets listed in `.gitignore`)


Check the content: ([bat](!https://github.com/sharkdp/bat) is just my preferred choice ^^)
```
bat .gitignore
bat wine-quality.csv.dvc
```
Add data to dvc and the placeholder file to git:
```
dvc add wine-quality.csv
git add wine-quality.csv.dvc
```

Add our example code to git (sanity checking is always a good idea):
```
git status
git add .
git commit -m “fresh experiment started”
```

Push data to dvc (local) storage:
```
dvc push
~Output:
  1 file pushed
```

Check output:
```
ls -R /tmp/dvc_demo_test

~Output:
  17
  /tmp/dvc_demo_test/17:
  fbffe83c746612cc247b182e9f7278
```


### Test pipeline

Execute [`dvc run`](!https://dvc.org/doc/command-reference/run)  to create stages. Stages are the unique steps of a pipeline and can be tracked via git.
Stages also connect code to its data input and output (similar to [Snakemake](!https://snakemake.readthedocs.io/en/stable/)).
The stages with all according dependencies and parameters get written to a special [pipeline file named dvc.yaml](!https://dvc.org/doc/user-guide/project-structure/pipelines-files).

I divided the code into different scripts to demonstrate the staging and pipelining process.

---

**Create dataset**
```
dvc run -f -n prepare\
-d create_dataset.py \
-o assets/data \
python create_dataset.py
```

-n the name of the stage

-d dependencies of this stage

-o output of the results

**Featurize**
```
dvc run -f -n featurize \
-d create_features.py \
-d assets/data \
-o assets/features \
python create_features.py
```

..as we can see we have now two dependencies, the feature-creating script and the output of the previous step.

**Train model**
```
dvc run -f -n train \
-d train_model.py \
-d assets/features \
-o assets/models \
-p model_type,random_state,train \
python train_model.py
```

-p use specified parameters from parameters.yaml file

Quick glance into parameters.yaml:
```
model_type: ElasticNet
lr: 0.0041
random_state: 42
train:
  epochs: 70
  alpha: 0.01
  l1_rate: 0.5
```

**Evaluate model**\
```
dvc run -f -n evaluate \
-d evaluate_model.py \
-d assets/features \
-d assets/models \
-p model_type \
-M assets/metrics.json \
python evaluate_model.py
```

-M writes metrics to a specified output destination, in our case mean_squared_error, mean_absolute_error, r2_score


---

Now, lets track our changes:
```
git add assets/.gitignore dvc.yaml dvc.lock
git commit -m “added stages to demo_test”
```

dvc.yaml now includes information about the commands we ran, its dependencies, and outputs.

```
bat dvc.yaml
~Output:
stages:
  prepare:
    cmd: python create_dataset.py
    deps:
    - create_dataset.py
    outs:
    - assets/data
  featurize:
    cmd: python create_features.py
    deps:
    - assets/data
    - create_features.py
    outs:
    - assets/features
  train:
    cmd: python train_model.py
    deps:
    - assets/features
    - train_model.py
    params:
    - model_type
    - random_state
    - train
    outs:
    - assets/models
  evaluate:
    cmd: python evaluate_model.py
    deps:
    - assets/features
    - assets/models
    - evaluate_model.py
    params:
    - model_type
    metrics:
    - assets/metrics.json:
        cache: false
```

There’s no need to use [`dvc add`](!https://dvc.org/doc/command-reference/add) for DVC to track stage outputs, [`dvc run`](!https://dvc.org/doc/command-reference/run#run) already took care of this.
You only need to run [`dvc push`](!https://dvc.org/doc/command-reference/push) if you want to save them to remote storage. (In our case we address our local storage)
```
dvc push
~Output:
  8 files pushed
```

Check dvc push:
`ls -R /tmp/dvc_demo_test`



### Test parameter changes

The whole point of creating the stages and the dvc.yaml file is for being able to reproduce and easily run the pipeline when changes occur.

When executing [`dvc repro`](!https://dvc.org/doc/command-reference/repro) with no change to the codebase or parameters:

..nothing happens.

Now lets open `params.yaml` and change some parameters (e.g alpha from 0.01 to 0.1) and re-run the pipeline.
```
dvc repro
~ Output:
 Stage ‘prepare’ didn’t change, skipping
 Stage ‘featurize’ didn’t change, skipping
 Running stage ‘train’:
   > python train_model.py
 Updating lock file ‘dvc.lock’
 
 To track the changes with git, run:
  git add dvc.lock
 Use `dvc push` to send your updates to the remote storage.
```

Look at the changes between our last commit and the current run:
```
dvc params diff — all

~Output:
 Path Param Old New
 params.yaml lr 0.0041 0.0041
 params.yaml model_type ElasticNet ElasticNet
 params.yaml random_state 42 42
 params.yaml train.alpha 0.01 0.1
 params.yaml train.epochs 70 70
 params.yaml train.l1_rate 0.5 0.5
```

Lets track our changes:
```
git add dvc.lock params.yaml
git commit -m “changed alpha parameter”
```

For the sake of it, we can print the stages as graph by executing dvc dag:
```
+---------+
         | prepare |
         +---------+
              *
              *
              *
        +-----------+
        | featurize |
        +-----------+
         **        **
       **            *
      *               **
+-------+               *
| train |             **
+-------+            *
         **        **
           **    **
             *  *
        +----------+
        | evaluate |
        +----------+
+----------------------+
| wine-quality.csv.dvc |
```

When given appropriate structure, DVC automatically determines which parts of a project need to be re-run. Runs and their results are cached to avoid unnecessary re-runs of stages. (automation)

`dvc.yaml` and `dvc.lock` files describe what data to use and which commands will generate the pipeline results. These files can be versioned and shared via git. (reproducibility)


### Test metric changes

We currently use mean_squared_error (RMSE) and mean_absolute_error (MAE) as metrics

Contents of assets/metrics.json after running the evaluate pipeline:
`{“rmse”: 0.10888875839569741, “mae”: 0.08314237592519587}`

Now lets add r2_score (R2) into our evaluate_model.py script and re-run the stages. Dvc realizes that the script has been tinkered with and re-runs only that one stage:

```
dvc repro
~Output:
 Stage ‘prepare’ didn’t change, skipping
 Stage ‘featurize’ didn’t change, skipping
 Stage ‘train’ didn’t change, skipping
 Running stage ‘evaluate’:
  > python evaluate_model.py
 
Updating lock file ‘dvc.lock’
```

This time, `assets/metrics.json` looks as follows:

`{“rmse”: 0.10888875839569741, “mae”: 0.08314237592519587, “r2”: 0.9829560472003764}`

### Test dataset changes

In the beginning, we created a (local) remote storage and executed dvc push to copy the locally cached data to that storage.
Let’s check if its there:

```
ls -R /tmp/dvc_demo_test
~Output:
 /tmp/dvc_demo_test/17:
 fbffe83c746612cc247b182e9f7278
 /tmp/dvc_demo_test/1a:
 240023ddb507d979001525a8ec2669
..
```

We can see several hashes here, so which one is our actual data?
A look into wine-quality.csv.dvc reveals:

`- md5: 17fbffe83c746612cc247b182e9f7278`

thus the first entry contains our data.

Now lets test how well retrieving works..
First, remove both cache and original data:

```
rm -rf .dvc/cache
rm -f wine-quality.csv
```

Then, get the data from the storage:

```
dvc pull
~Output:
 A wine-quality.csv
 1 file added and 6 files fetched
```

Now lets alter the dataset by adding one additional imaginary bottle at the beginning of wine-quality.csv ..

```
“fixed acidity”,”volatile acidity”,”citric acid”,”residual sugar”,”chlorides”,”free sulfur dioxide”,”total sulfur dioxide”,”density”,”pH”,”sulphates”,”alcohol”,”quality”
7.1,0.28,0.33,19.7,0.046,45,170,1.001,3,0.45,8.8,6 #our fake bottle
7,0.27,0.36,20.7,0.045,45,170,1.001,3,0.45,8.8,6
```

..and add the actual version to the storage:

```
dvc add wine-quality.csv
~Output:
 100% Add|  ████████████████████████████████████████████████████████████████████████████████████████████████████|1/1 [00:08, 8.27s/file]
```

Track the changes with git..

```
git add wine-quality.csv.dvc
git commit -m “updated dataset with fake bottle”
```

..and push the actual version to the storage:

```
dvc push
~Output:
 1 file pushed
```

Oops, we just learned our fake bottle turns out to be vinegar. Let’s roll back to a previous version of our dataset.

First, sanity- check your current state with git log to see where our current HEAD is. 
Then, go one step back to the previous state of the .dvc file:

```
git checkout HEAD~1 wine-quality.csv.dvc
~Output:
 Updated 1 path from cb50800
dvc checkout

~Output:
 M wine-quality.csv
```

Looking into wine-quality.csv, our fake bottle is gone. :)

Don’t forget to commit your changes:

`git commit -m “reverting dataset update"`

## Outlook
This was the first part of the series, we went througth some basic usage of DVC. In the next parts (as soon as I find the time) things like DVC’s pretty neat experiments capability, working with remote storage and using DVC within a HPC (High Performance Computing) environment will be covered.

I hope this article can be of help to someone :) Feedback is always welcome!
