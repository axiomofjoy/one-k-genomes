"""
This script runs hyperparameter search experiments using TensorFlow,
Keras, and Talos.
"""


import tensorflow as tf
import keras
from keras.utils import to_categorical
from keras.optimizers import Adam
from keras.regularizers import l2
from keras.layers import Dropout, Dense
from sklearn.model_selection import train_test_split
import talos
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def genomes_model(X_train, y_train, X_val, y_val, p):
    """
    This function defines a fully connected neural network.

    This function defines a fully connected neural network with three
    hidden layers. It outputs the trained model and model history, and
    is designed for use with :code:`talos.Scan`.

    :param X_train: :code:`numpy` array containing training data.
    :param y_train: :code:`numpy` array containing trainig labels.
    :param X_val: :code:`numpy` array containing validation data.
    :param y_val: :code:`numpy` array containing validation labels.
    :param p: Dictionary of parameter values.

    :return out: The output of fitting a :code:`keras` model.
    :return model: The fitted :code:`keras` model.
    """


    model = keras.Sequential([
        Dropout(p["dropout_input"]),
        Dense(2400, kernel_regularizer=l2(p["reg"]), activation=tf.nn.relu),
        Dropout(p["dropout_hidden"]),
        Dense(600, kernel_regularizer=l2(p["reg"]), activation=tf.nn.relu),
        Dropout(p["dropout_hidden"]),
        Dense(100, kernel_regularizer=l2(p["reg"]), activation=tf.nn.relu),
        Dropout(p["dropout_hidden"]),        
        Dense(26, kernel_regularizer=l2(p["reg"]), activation=tf.nn.softmax)
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


def main():

    # Load data.
    X = np.load("/home/ubuntu/one-k-genomes/data/dim_reduc/complete_pca/"
                "embedded_num.npy")

    # Load ground truth labels.
    df = pd.read_csv("/home/ubuntu/one-k-genomes/data/sample_data/"
                     "sample_data.tsv", sep='\t')
    pops = list(set(df["Population"].tolist()))
    pops.sort()
    num_classes = len(pops)
    targets = np.array([pops.index(pop) for pop in df["Population"].tolist()])
    y = to_categorical(targets)

    # Create a 60-20-20 train-validation-test split.
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=0.2, random_state=0
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=0.25, random_state=0
    )

   # Define the hyperparameter search space.
    p = {
        "dropout_input": np.linspace(0.0, 0.2, 3),
        "dropout_hidden": np.linspace(0, 0.5, 6),
        "reg": np.linspace(0, 0.25, 6),
        "lr": 10 ** np.linspace(-4, np.log10(5) - 3, 10),
        "epochs": [100]
    }

    # Run experiments. This may take a while.
    param_search = talos.Scan(
        x=X_train,
        y=y_train,
        x_val=X_val,
        y_val=y_val,
        model=genomes_model,
        params=p,
        grid_downsample=0.2
    )

    # Save experiment results to disk.
    df = param_search.data
    df.sort_values(by=["val_acc"], inplace=True, ascending=False)
    df.to_csv("output/model1_test3.csv")


if __name__ == "__main__":
    main()
