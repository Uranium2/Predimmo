from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import os

script_dir = os.path.dirname(__file__)
data = pd.read_csv(os.path.join(script_dir,"..\\datasets\\lbc_75_append.csv"))

y = data[["valeur_fonciere"]]
X = data[["code_postal", "type_local", "surface", "nombre_pieces_principales", "month", "year"]]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

print(X_train)
print(y_train)
