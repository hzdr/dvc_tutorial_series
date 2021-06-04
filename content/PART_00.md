This is the 1/n part of my dvc tutorial series. (A work in progress)

**DVC (Data Version Control) is basically version control expanded to the use-cases of machine learning (and similar pipelines)**

During the past months I started evaluating different frameworks to manage machine learning workflows for our usecase at [HelmholtzAI](!https://www.helmholtz.ai). DVC turned out to become one of the final candidates, so I decided to convert what I've learned on my way into a mini-series.  

I decided to dive right in with a tutorial which tackles different aspects important to evaluate the suitability of the framework. 

You can find the code on our [GitHub](!link) and follow along.

I also decided to share my general approach on how to tackle this kind of task and why the tutorial is designed the way it is - if you are only interested in the code, feel free to jump right to the section **DVC TUTORIAL**



### Usecase

An important aspect of choosing tools is always to have your use-case in mind. I currently work at a research facility, so our use cases include large scientific datasets, custom infrastructure (own datacenters, HPC) and a particular need for reproducibility. Following from this, the boxes a tool must tick, are:

- reproducibility:
    - Verifable results are crucial for research. If the results were obtained by using ML along the way, this part must also be reproducible for independent researchers. A typical ML project contains code, dataset, (tuning) parameters and model(s)

- workflow integration:
    - as the tool might be used both by IT professionals and scientists, it needs to be as non-invasive as possible - you can't expect a scientist with some basic coding skills to detangle framework specific code from ML code.

- exchangable backend:
    - we have our own datacenters and cloud infrastructure, thus the tooling must be able to work with custom storage solutions. 

- framework agnostic:
    - it shouldn't care if we use pytorch, tensorflow or sth custom. If it's also language agnostic, this would be preferred.

- open source:
    - we think it's the right thing to do and support. Also, usually it's much easier to adapt to custom needs.

- other:
    - we prefer solutions that we can tweak towards our needs
    - budget matters


### Tutorial setup
As I am actually testing multiple frameworks against each other, there needs to be a good base for comparison. Thus, the example, parameters and things to test should be aligned across test scenarios (and adjusted where necessary as every tool integrates differently). For this case I created a initial protocol: 


```
#### Pipeline
- integratie $tool into workflow
- run ml-pipeline with $tool

#### Parameters
Test logging, altering and retrieving:
    - parameter 1 (val0, val1, val2)
    - parameter 2 (val0, val1, val2)
    
#### Metrics
Test logging, exchanging and retrieving:
    - metric 1
    - metric 2
    - (metric 3) 

#### Models
Test exchangeability of models
- model 1 (type, parameters, metrics)
- model 2 (type, parameters, metrics)

#### Dataset
Storing, altering, versioning and retrieving 
- small dataset (PoC)
- large dataset
```

### The example
I wanted to use something (relatively) official and well tested, thus I decided to utilise an [example](!https://www.mlflow.org/docs/latest/tutorials-and-examples/tutorial.html) found in the tutorials section of another tool [MLflow](!https://mlflow.org/) which is also a hot candidate. (I consider also publishing the whole comparison setup of the frameworks, but thats for another time. ^^)

It turned out that the example needed some closer examination and adjustments. As I feel its important to understand what one is working with in order to know what to look for, you can find details in [/content/EXAMPLE.md](!content/EXAMPLE.md). 

Let's get to work!

### DVC TUTORIAL

I currently use OSX and manage my environments with [conda](!https://docs.conda.io/en/latest/). I provided a very basic `environment.yml` for those who use conda too, if you use something else, just have a look at `environment.yml` to see which additional packages you'll need. 

**Make sure to have DVC installed within your working environment**
Have a look at their [documentation](!https://dvc.org/doc/install) 

### Preparation:

Clone the repository:
`git clone ....`

### TEST PIPELINE

Initialise git:
`git init`

initialise dvc:
`dvc init`

Add remote storage (local in this case):
`mkdir /tmp/dvc_demo_test`
`dvc remote add -d localremote /tmp/dvc_demo_test`
`dvc remote list`

> DVC stores information about the added file (or a directory) in a special file named `data/data.xml.dvc`, a small text file with a human-readable format. This file can be easily versioned like source code with Git, as a placeholder for the original data (which gets listed in `.gitignore`):

Checking output:
```
bat .gitignore
bat wine-quality.csv.dvc
```

Add data:
```
dvc add wine-quality.csv
git add wine-quality.csv.dvc
```

Add example code:
`git status`
`git add .`
`git commit -m "fresh experiment started"`


Push data to dvc (local) storage:
`dvc push`

Output:
`1 file pushed`

Check output:
`ls -R /tmp/dvc_demo_test`

Output:
```
17

/tmp/dvc_demo_test/17:
fbffe83c746612cc247b182e9f7278
```

---
### Test pipeline

Use `dvc run` to create stages. Stages are the steps of a pipeline and can be tracked via git.  
Stages also connect code to its data input and output (similar to [snakemake](!https://snakemake.readthedocs.io/en/stable/)). 
The stages with all according dependencies and parameters get written to a `dvc.yaml` file at the end.
I divided the code into different scripts to demonstrate the staging and pipelining process. 

Create dataset:

```
dvc run -f -n prepare\
    -d create_dataset.py \
    -o assets/data \
    python create_dataset.py

```
-n the name of the stage
-d dependencies of this stage
-o output of the results

Featurize:
```
dvc run -f -n featurize \
    -d create_features.py \
    -d assets/data \
    -o assets/features \
    python create_features.py
```
..as we can see we have now two dependencied, the feature-creating script and the output of the previous step

Train model:
```
dvc run -f -n train \
    -d train_model.py \
    -d assets/features \
    -o assets/models \
    -p model_type,random_state,train \
    python train_model.py
```
-p train addresses all parameters under train: section in . yaml file

`bat parameters.yaml` to show section

Evaluate model:
```
dvc run -f -n evaluate \
    -d evaluate_model.py \
    -d assets/features \
    -d assets/models \
    -p model_type \
    -M assets/metrics.json \
    python evaluate_model.py
```
-M writes metrics, in our case mean_squared_error, mean_absolute_error, r2_score
into a .json file

Now, lets track our changes:
```
git add assets/.gitignore dvc.yaml dvc.lock
git commit -m "added stages to demo_test"
```

Check contents of `dvc.yaml`:
`bat dvc.yaml`

It includes information about the commands we ran, its dependencies, and outputs.
There's no need to use `dvc add` for DVC to track stage outputs, `dvc run` already took care of this. 
You only need to run `dvc push` if you want to save them to remote storage. (Here our local storage)

`dvc push  `
output:
`8 files pushed`

Check dvc push:
`ls -R /tmp/dvc_demo_test`

### Test parameter change

** Reproduce steps** 
The whole point of creating the stages and the dvc.yaml file is for being able to reproduce and easily run the pipeline when changes occur

Executed with no change:
`dvc repro`

..nothing happens

now lets open `params.yaml` and change some parameters (eg alpha from 0.01 to 0.1):

`vim params.yaml`

re-run pipeline..:
`dvc repro`

Output:
```
Stage 'prepare' didn't change, skipping
Stage 'featurize' didn't change, skipping
Running stage 'train':
> python train_model.py
Updating lock file 'dvc.lock'

To track the changes with git, run:

    git add dvc.lock
Use `dvc push` to send your updates to the remote storage.
```

Look at the changes between our last commit and the current run:
`dvc params diff --all`

Output:
```
Path         Param          Old         New
params.yaml  lr             0.0041      0.0041
params.yaml  model_type     ElasticNet  ElasticNet
params.yaml  random_state   42          42
params.yaml  train.alpha    0.01        0.1
params.yaml  train.epochs   70          70
params.yaml  train.l1_rate  0.5         0.5
```

Lets track our changes
```
git add dvc.lock params.yaml
git commit -m "changed alpha parameter"
```

For the sake of it, we can print the stages as graph:
`dvc dag`

--> ..so when given appropriate structure,  DVC automatically determines which parts of a project need to be run, and it caches "runs" and their results, to avoid unnecessary re-runs of stages (automation)

--> .. dvc.yaml and dvc.lock files describe what data to use and which commands will generate the pipeline results. This files can be versioned and shared via git (reproducibility)

### Test metric change
We currently use mean_squared_error (RMSE) and mean_absolute_error (MAE) as metrics

`assets/metrics.json` after running the evaluate pipeline:

```
{"rmse": 0.10888875839569741, "mae": 0.08314237592519587}
```

..lets add r2_score (R2) into our `evaluate_model.py` script and rerun the stages
dvc realises that the script has been tinkered with and re-runs only that one stage

`dvc repro`

```
Stage 'prepare' didn't change, skipping
Stage 'featurize' didn't change, skipping
Stage 'train' didn't change, skipping
Running stage 'evaluate':
> python evaluate_model.py
Updating lock file 'dvc.lock'
```

now `assets/metrics.json` looks as follows:
```
{"rmse": 0.10888875839569741, "mae": 0.08314237592519587, "r2": 0.9829560472003764}
```

### Test dataset changes
In the beginning, we created a (local) remote storage and used `dvc push` to copy the data cached locally to that very storage. 
Let's check if its there:

`ls -R /tmp/dvc_demo_test`

Output:
```
/tmp/dvc_demo_test/17:
fbffe83c746612cc247b182e9f7278

/tmp/dvc_demo_test/1a:
240023ddb507d979001525a8ec2669
...

```

There are several hashes here, so which one is our actual data?
A look into `wine-quality.csv.dvc` reveals 17fbffe83c746612cc247b182e9f7278,
thus the first entry is our data.

Now lets test how well retrieving works..
First, remove both cache and original data:

```
rm -rf .dvc/cache
rm -f wine-quality.csv
```

Then, get the data from the storage:
`dvc pull`

Output:
```
A       wine-quality.csv
1 file added and 6 files fetched
```

Now lets alter that dataset by adding one additional imaginary bottle at the beginning
of `wine-quality.csv:

```
"fixed acidity","volatile acidity","citric acid","residual sugar","chlorides","free sulfur dioxide","total sulfur dioxide","density","pH","sulphates","alcohol","quality"
7.1,0.28,0.33,19.7,0.046,45,170,1.001,3,0.45,8.8,6  # our fake bottle
7,0.27,0.36,20.7,0.045,45,170,1.001,3,0.45,8.8,6
```

..and add the actual version to the storage:

`dvc add wine-quality.csv`

Output:
```
100% Add|████████████████████████████████████████████████████████████████████████████████████████████████████|1/1 [00:08,  8.27s/file]
```

track it as usual with git..:
```
git add wine-quality.csv.dvc
git commit -m "updated dataset with fake bottle"
```
..and finally push the actual version to the storage:
`dvc push`

Output:
`1 file pushed`

Now, we just learned our fake bottle turns out to be vignear. 
Let's roll back to a previous version of our dataset. 
First, check your current state with `git log` to see where our current HEAD is.
Then, go one step back to the previous state of the .dvc file:
```
git checkout HEAD~1 wine-quality.csv.dvc
    Updated 1 path from cb50800

dvc checkout
    M       wine-quality.csv
```

Looking into wine-quality.csv, our fake bottle is indeed, gone.
Don't forget to commit your changes:

`git commit -m "reverting dataset update"`

---

## Outlook
This was the first part of the series, walking througth some basic usage of DVC. In the next parts (when I find the time) I plan to cover things like DVC's pretty neat experiments capability, working with remote storage and using DVC within a HPC (High Performance Computing) environment.

I hope this proofes useful to someone, feedback is always welcome!

