import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime

# connect to your database
conn = sqlite3.connect("options_data.db")

# load data
df = pd.read_sql("SELECT * FROM options_data", conn)

print(df.head())

# convert dates
df["expiry"] = pd.to_datetime(df["expiry"])
df["snapshot_date"] = pd.to_datetime(df["snapshot_date"])

# time to expiry in years
df["T"] = (df["expiry"] - df["snapshot_date"]).dt.days / 365

# encode option type
df["is_call"] = (df["type"] == "call").astype(int)

# risk-free rate (constant for now)
df["r"] = 0.05

# select features and target
features = ["strike", "T", "r", "is_call", "impliedVolatility"]
X = df[features].fillna(0).values
y = df["lastPrice"].values


from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, shuffle=False  # no lookahead
)


import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

model = keras.Sequential([
    layers.Dense(64, activation="relu", input_shape=(X_train.shape[1],)),
    layers.Dense(64, activation="relu"),
    layers.Dense(1)  # output = predicted price
])

model.compile(optimizer="adam", loss="mse", metrics=["mae"])
