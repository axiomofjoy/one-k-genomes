import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle

# Method to load pickle file.
def load_obj(file):
    with open(file, 'rb') as fid:
        return pickle.load(fid)

def main():
    path = '/home/ubuntu/onekgenomes/'
    # Load data.
    X = np.load(path + 'data/dimReduc/dualPCA/embeddedNum.npy')

    # Get labels.
    df = pd.read_csv(path + "data/sampleData/sampleData.csv")
    pops = list(set(df["Population"].tolist()))
    pops.sort()
    num_classes = len(pops)
    targets = np.array([pops.index(pop) for pop in df["Population"].tolist()])
    y = to_categorical(targets)

    # Train-test split.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.4, random_state=0)
    num_samples, num_features = X_train.shape

    # Define neural network.
    model = keras.Sequential([
        keras.layers.Dense(3000, activation=tf.nn.relu, input_shape=(num_features,)),
#        keras.layers.Dropout(0.5),
        keras.layers.Dense(1000, activation=tf.nn.relu),
#        keras.layers.Dropout(0.5),
        keras.layers.Dense(300, activation=tf.nn.relu),
#        keras.layers.Dropout(0.5),
        keras.layers.Dense(100, activation=tf.nn.relu),
        keras.layers.Dense(26, activation=tf.nn.softmax)
    ])

    # Compile model.
    optimizer = Adam(lr=0.00015)
    model.compile(optimizer=optimizer,
        loss='categorical_crossentropy',
        metrics=['accuracy'])

    # Train.
    history = model.fit(X_test, y_test, batch_size=num_samples, epochs=200)
    train_loss, train_acc = model.evaluate(X_train, y_train)

    print('Train loss:', train_loss)
    print('Train accuracy:', train_acc)

if __name__ == "__main__":
    main()
