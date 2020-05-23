import pandas as pd
import numpy as np
import os
import tensorflow as tf
from sklearn import preprocessing


def build_model(shape):
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(128, activation='relu', input_shape=[shape]),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
  ])
    optimizer = tf.keras.optimizers.Adam(0.01)

    model.compile(loss='mse',
        optimizer=optimizer,
        metrics=['accuracy'])
    return model

script_dir = os.path.dirname(__file__)
data = pd.read_csv(os.path.join(script_dir,"..\\datasets\\75.csv"))

col_param = ["longitude", "latitude"]

y = data[["valeur_fonciere"]]
X = data[col_param]

# type_local = X["type_local"].unique()
# type_local_dict = dict(zip(type_local, range(len(type_local))))
# X = X.replace(type_local_dict)

for i in col_param:
    X[i] = X[i].fillna(X[i].mean())

print(X)

y["valeur_fonciere"] = y["valeur_fonciere"].fillna(y["valeur_fonciere"].mean())

min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(X.values)
X = pd.DataFrame(x_scaled)


# min_max_scaler = preprocessing.MinMaxScaler()
# y_scaled = min_max_scaler.fit_transform(y.values)
# y = pd.DataFrame(y_scaled)

print(X)

model = build_model(len(X.keys()))

model.summary()

model.fit(x=X, y=y, epochs=10, batch_size=100, verbose=1, validation_split=0.20)
