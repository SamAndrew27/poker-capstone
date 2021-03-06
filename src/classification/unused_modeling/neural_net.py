from data_prep import training_data_Xy
import pandas as pd 
import numpy as np 
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from tensorflow.keras.metrics import Precision, AUC
from tensorflow.keras import backend as K 
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.model_selection import StratifiedKFold
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import f1_score

# load dataset
X, y = training_data_Xy(scale=True)
# encode class values as integers

# baseline model
def create_baseline():
	# create model
    model = Sequential()
    # model.add(Dropout(0.2, input_shape=(10,)))

    model.add(Dense(20, input_dim=10, activation='relu'))
    # model.add(Dense(20, activation='relu'))
    # model.add(Dense(100, activation='softmax'))
    # model.add(Dropout(0.2, input_shape=(10,)))
    model.add(Dense(10, activation='relu'))



    model.add(Dense(1, activation='sigmoid'))
    # Compile model
    opt = Adam(lr=.00001)
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=[AUC(), Precision(),f1_m])
    return model
# evaluate model with standardized dataset

def recall_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def precision_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))

def model_eval(X, y):
    skf = StratifiedKFold(n_splits=5, shuffle=True)
    cvscores = []
    for train, test in skf.split(X, y):
        model = create_baseline()
        es = EarlyStopping(monitor='loss', mode='min', verbose=0, patience=50)
        # Fit the model
        model.fit(X.iloc[train], y.iloc[train], verbose=0, epochs=100, batch_size=100, callbacks=[es])
        # evaluate the model
        scores = model.evaluate(X.iloc[test], y.iloc[test], verbose=1)
        print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
        cvscores.append(scores[1] * 100)
    print("%.2f%% (+/- %.2f%%)" % (np.mean(cvscores), np.std(cvscores)))



if __name__=="__main__":
    # estimator = KerasClassifier(build_fn=create_baseline, epochs=100, batch_size=50, verbose=1)
    # kfold = StratifiedKFold(n_splits=5, shuffle=True)
    # results = cross_val_score(estimator, X, y, cv=kfold, scoring='f1')
    # print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))
    model_eval(X,y)

    # soft max seems to work just as well as relu 
    # more small layers seems worse 
    # def create_baseline():
    # 	# create model
    #     model = Sequential()
    #     model.add(Dropout(0.2, input_shape=(10,)))

    #     model.add(Dense(10, input_dim=10, activation='relu'))
    #     model.add(Dense(20, activation='relu'))
    #     model.add(Dense(100, activation='softmax'))
    #     model.add(Dropout(0.2, input_shape=(10,)))
    #     model.add(Dense(20, activation='relu'))

    # epochs=5000, batch_size=30

    #     model.add(Dense(1, activation='sigmoid'))
    #     # Compile model
    #     opt = Adam(lr=.00001)
    #     model.compile(loss='binary_crossentropy', optimizer=opt, metrics=[AUC(), Precision()])
    #     return model
    # # evaluate model with standardized dataset