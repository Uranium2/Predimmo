import xgboost as xgb
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import os

script_dir = os.path.dirname(__file__)
data = pd.read_csv(os.path.join(script_dir,"..\\datasets\\lbc_75_append.csv"))

y = data[["valeur_fonciere"]]
X = data[["code_postal", "type_local", "surface", "nombre_pieces_principales", "month", "year"]]

data_dmatrix = xgb.DMatrix(data=X,label=y)


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

xg_reg = xgb.XGBRegressor(objective ='reg:squarederror', colsample_bytree = 0.3, learning_rate = 0.1,
                max_depth = 5, alpha = 10, n_estimators = 10)

xg_reg.fit(X_train,y_train)

preds = xg_reg.predict(X_test)


print(y_test)
print(preds)

rmse = np.sqrt(mean_squared_error(y_test, preds))
print("RMSE: %f" % (rmse))

