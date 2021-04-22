from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
import pandas as pd 
from tensorflow.keras import backend as K
import numpy as np 
from regression_prep import trying_to_get_NN_to_work



X, y = trying_to_get_NN_to_work()


def baseline_model():
	# create model
	model = Sequential()
	model.add(Dense(8, input_dim=8, kernel_initializer='normal', activation='relu'))
	model.add(Dense(1, kernel_initializer='normal'))
	# Compile model
	model.compile(loss='mean_squared_error', optimizer='adam', metrics=[coeff_determination])
	return model








def coeff_determination(y_true, y_pred):
    SS_res =  K.sum(K.square( y_true-y_pred )) 
    SS_tot = K.sum(K.square( y_true - K.mean(y_true) ) ) 
    return ( 1 - SS_res/(SS_tot + K.epsilon()) )

if __name__ == '__main__':

# evaluate model
    estimator = KerasRegressor(build_fn=baseline_model, epochs=100, batch_size=5, verbose=0)
    kfold = KFold(n_splits=5)
    results = cross_val_score(estimator, X, y, cv=kfold)
    print("Baseline: %.2f (%.2f) MSE" % (results.mean(), results.std()))