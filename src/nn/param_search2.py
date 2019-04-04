import tensorflow as tf
import keras
from keras.models import Model
from keras.utils import to_categorical
from keras.optimizers import Adam
from keras.regularizers import l2
from keras.layers import Dropout, Dense, Input, BatchNormalization, Activation
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import talos
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle


# Method to load pickle file.
def load_obj(file):
    with open(file, 'rb') as fid:
        return pickle.load(fid)

# Get data.
X = np.load("/home/ubuntu/onekgenomes/data/dimReduc/completePCA/embeddedNum.npy")

# Get labels.
df = pd.read_csv("/home/ubuntu/onekgenomes/data/sampleData/sampleData.tsv", sep='\t')
pops = list(set(df["Population"].tolist()))
pops.sort()
num_classes = len(pops)
targets = np.array([pops.index(pop) for pop in df["Population"].tolist()])
y = to_categorical(targets)

# Train-validation-test split (60-20-20).
X_temp, X_test, y_temp, y_test = train_test_split(
    X, y, test_size=0.2, random_state=0
)
X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp, test_size=0.25, random_state=0
)

# Normalize inputs.
scaler = StandardScaler()
scaler.fit(X_train)
X_train, X_val, X_test = scaler.transform(X_train), scaler.transform(X_val), scaler.transform(X_test)

# Define model.
def genomes_model(X_train, y_train, X_val, y_val, p):
    model = keras.Sequential([
        Dropout(p["dropout_input"]),
        Dense(2400, kernel_regularizer=l2(p["reg"])),
        BatchNormalization(),
        Activation('relu'),
        Dropout(p["dropout_hidden"]),
        Dense(600, kernel_regularizer=l2(p["reg"])),
        BatchNormalization(),
        Activation('relu'),
        Dropout(p["dropout_hidden"]),
        Dense(100, kernel_regularizer=l2(p["reg"])),
        BatchNormalization(),
        Activation('relu'),
        Dropout(p["dropout_hidden"]),
        Dense(26, kernel_regularizer=l2(p["reg"])),
        BatchNormalization(),
        Activation('softmax')
    ])
    num_train = X_train.shape[0]
    optimizer = Adam(lr=p["lr"])
    model.compile(optimizer=optimizer,
        loss='categorical_crossentropy',
        metrics=['accuracy'])
    out = model.fit(
        X_train,
        y_train,
        validation_data=[X_val, y_val],
        batch_size=num_train,    # Batch gradient descent.
        epochs=p["epochs"]
    )
    
    return out, model


"""# First parameter search space.
p = {
    "dropout_input": list(np.linspace(0, 0.23333333, 8)),
    "dropout_hidden": list(np.linspace(0, 0.5, 16)),
    "reg": list(10 ** np.linspace(-4,3,22)),
    "lr": list(10 ** np.linspace(-3,-5, 7)),
    "epochs": [100]
}
"""

# Second parameter search space.
p = {
    "dropout_input": np.linspace(0,0.25,26),
    "dropout_hidden": np.linspace(0,0.5,51),
    "reg": 10 ** np.linspace(-3,3,19),
    "lr": 10 ** np.linspace(-4,2,19),
    "epochs": [100]
}

# Scan.
param_search = talos.Scan(
    x=X_train,
    y=y_train,
    x_val=X_val,
    y_val=y_val,
    model=genomes_model,
    params=p,
    grid_downsample=0.0004,    # Percent of parameter space to search.
    seed=0
)

# Save data.
df = param_search.data
df.sort_values(by=["val_acc"], inplace=True, ascending=False)
df.to_csv("output/parameters_search3.csv")

