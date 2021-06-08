This is the codepart of the article series I published on medium [here]. (https://nsultova.medium.com/exploring-dvc-for-machine-learning-pipelines-in-research-part-1-3ebc2ca35a18) 


During the past months part of my job became looking at different tools to manage machine learning workflows for our team at [HelmholtzAI](https://www.helmholtz.ai/). 

A lot of material accumulated on the way, thus I decided to share some of the process and what I’ve learned.

This repository contains tutorials and code centered around [DVC](https://dvc.org) which became one of our favourite candidates.


### Code structure

```
.
├── README.md
├── content
│   ├── PART_00.md
│   └── EXAMPLE.md
│   └── RESSOURCES.md
└── src
    ├── assets
    ├── config.py
    ├── create_dataset.py
    ├── create_features.py
    ├── environment.yml
    ├── evaluate_model.py
    ├── params.yaml
    ├── train_model.py
    └── wine-quality.csv
```

- `/content`:  contains the articles and additional informations
- `/assets`: directiory where (intermediate) results are being written to
- `environment.yml` - can be used to create a conda environment or just to look up which dependencies are needed
- `config.py` - handle paths and other variables, makes eventual expanding less cumbersome
- `params.yaml` - used by .dvc, custom parameters can be set here

..the rest should be self-explanatory.

### Setup

Make sure you have some recent python version installed. (I run Python 3.9.1 within an conda environment on an macOS Big Sur 11.4 as of this writing). 

I'd highly recommend to use any flavour of virtual environments (conda, venv, ..) for following along with this tutorial. (Except you're a *-BSD or NixOS user, in thus case I assume you know your way around these issues anyway ^^ ). 

Clone the repo, make sure the dependencies are installed and you're good to go!

Look into `/content/PART_01`, section **DVC Tutorial** for more information.
