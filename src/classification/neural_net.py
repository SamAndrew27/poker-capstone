from capstone3_data_prep import read_in_return_Xy_scaled_no_unused
import pandas as pd 
# from keras.models import Sequential
# from keras.layers import Dense
# from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold

# load dataset
X, y = read_in_return_Xy_scaled_no_unused()
# encode class values as integers

# baseline model
# def create_baseline():
# 	# create model
# 	model = Sequential()
# 	model.add(Dense(60, input_dim=60, activation='relu'))
# 	model.add(Dense(1, activation='sigmoid'))
# 	# Compile model
# 	model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# 	return model
# evaluate model with standardized dataset



if __name__=="__main__":

# estimator = KerasClassifier(build_fn=create_baseline, epochs=100, batch_size=5, verbose=1)
# kfold = StratifiedKFold(n_splits=10, shuffle=True)
# results = cross_val_score(estimator, X, encoded_Y, cv=kfold)
# print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))
    print(X.info())