import pickle
import json
import yaml
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, accuracy_score,confusion_matrix
from sklearn.linear_model import ElasticNet, LogisticRegression

import pandas as pd
import numpy as np

from config import Config


def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2

with open ("params.yaml", "r") as fd:
    params = yaml.safe_load(fd)

model_type = params['model_type']
alpha = params['train']['alpha']
l1_rate = params['train']['l1_rate']

X_test = pd.read_csv(str(Config.FEATURES_PATH / "test_features.csv"))
y_test = pd.read_csv(str(Config.FEATURES_PATH / "test_labels.csv"))

model = pickle.load(open(str(Config.MODELS_PATH / "model.pickle"), "rb"))

y_pred = model.predict(X_test)
(rmse, mae, r2) = eval_metrics(y_test, y_pred)
#acc = accuracy_score(y_test,y_pred)
#cnf_mat = confusion_matrix(y_test,y_pred)

if model_type == "ElasticNet":
    pass
    #print(f"ElasticNet model : alpha = {alpha}, l1_rate = {l1_rate}")

if model_type == "RandomForestRegressor":
    print(f"RandomForestRegressor model")

print(f"RMSE : {rmse}\nMAE : {mae}\nR2 : {r2}")
#print(f"Accuracy score: {accuracy_score}")
#print(f"Confision matrix : {cnf_mat}")

#For dvc we just write this out as regular data and track it later
with open(str(Config.METRICS_FILE_PATH), "w") as outfile:
    json.dump(dict(rmse=rmse, mae=mae,r2=r2), outfile)

#with open(str(Config.PLOTS_FILE_PATH), "w") as outfile:
#    json.dump(dict(accuracy_score=accuracy_score, confusion_matrix=cnf_mat), outfile)

"""
ax0.set_ylabel('Target predicted')
ax0.set_xlabel('True Target')
ax0.set_title('Ridge regression \n without target transformation')
ax0.text(100, 1750, r'$R^2$=%.2f, MAE=%.2f' % (
r2_score(y_test, y_pred), median_absolute_error(y_test, y_pred)))
"""
