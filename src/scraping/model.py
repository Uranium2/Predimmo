import pandas as pd
import numpy as np
import os
import tensorflow as tf

def build_model(shape):
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=[shape]),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(1)
    ])

    optimizer = tf.keras.optimizers.RMSprop(0.001)

    model.compile(loss='mse',
                optimizer=optimizer,
                metrics=['mae', 'mse'])
    return model

script_dir = os.path.dirname(__file__)
data = pd.read_csv(os.path.join(script_dir,"..\\datasets\\lbc_75_append.csv"))

y = data[["valeur_fonciere"]]
X = data[["code_postal", "type_local", "surface", "nombre_pieces_principales", "month", "year"]]

model = build_model(len(X.keys()))

model.fit(x=X, y=y, epochs=100, batch_size=1000, verbose=1, validation_split=0.20)
