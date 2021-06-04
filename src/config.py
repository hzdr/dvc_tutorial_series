from pathlib import Path

#Parameters and folders for the different experiments for dvc-example
#RANDOM_SEED = 42
#ALPHA = 0.3
#L1_RATIO = 0.03

class Config:
    MODEL_TYPE = "ElasticNet" #"RandomForestRegressor" #"LogisticRegression"
    #for dvc one could also handle and track this via specifying a set of parameter dependencies 
    # the stage depends on, from a parameters file. See  dvc official docs for more
    #RANDOM_SEED = RANDOM_SEED
    #ALPHA = ALPHA
    #L1_RATIO = L1_RATIO
    DVC_ASSETS_PATH = Path("./assets")

    ORIGINAL_DATASET_FILE_PATH = Path("wine-quality.csv")
    DATASET_PATH = Path(DVC_ASSETS_PATH / "data")
    FEATURES_PATH = Path(DVC_ASSETS_PATH / "features")
    MODELS_PATH = Path(DVC_ASSETS_PATH / "models")
    METRICS_FILE_PATH = Path(DVC_ASSETS_PATH / "metrics.json")
    PLOTS_FILE_PATH = Path(DVC_ASSETS_PATH / "plots.json")