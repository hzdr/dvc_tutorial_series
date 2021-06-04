This is the code-part of the mini-series I published [here](!) (Yet to be published officially) 

This repository contains tutorials + code which I created based on my explorations of [DVC](!https://dvc.org)


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

Make sure you have some recent python version installed. (I run Python 3.9.1 within an conda environment on an OSX (add version) as of this writing). 
I'd highly recommend to use any flavour of virtual environments (conda, venv, ..(except you're a *-BSD or NixOS user ^^ )). 

Clone the repo, make sure the dependencies are installed and you're good to go!

Look into `/content/PART_00`, section **DVC Tutorial** for more information.
