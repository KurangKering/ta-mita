import numpy as np
import pandas as pd
from random import randrange
from neupy import algorithms

np.random.seed(0)

data_train = pd.read_csv('output/data-train-90.csv')
data_test = pd.read_csv('output/data-test-10.csv')

train_data = data_train.loc[:, ~data_train.columns.isin(['ID'])]

X_train = train_data.iloc[:, :-1].to_numpy()
Y_train = train_data.iloc[:, -1].to_numpy()


test_data = data_test.loc[:, ~data_test.columns.isin(['ID'])]

X_test = test_data.iloc[:, :-1].to_numpy()
Y_test = test_data.iloc[:, -1].to_numpy()


lvqnet = algorithms.LVQ2(n_inputs=X_train.shape[1], n_classes=np.unique(Y_train).size, verbose=True)
lvqnet.train(X_train, Y_train, epochs=100)
print(lvqnet.predict(X_test))