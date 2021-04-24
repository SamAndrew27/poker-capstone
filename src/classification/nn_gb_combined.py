from data_prep import read_in_return_Xy_scaled_no_unused
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
from sklearn.ensemble import GradientBoostingClassifier
# load dataset
X, y = read_in_return_Xy_scaled_no_unused()
# encode class values as integers

# baseline model
def create_baseline():
	# create model
    model = Sequential()
    # model.add(Dropout(0.1, input_shape=(10,)))

    model.add(Dense(11, input_dim=11, activation='relu'))
    model.add(Dense(22, activation='relu'))



    model.add(Dense(1, activation='sigmoid'))
    # Compile model
    opt = Adam(lr=.001)
    model.compile(loss='binary_crossentropy', optimizer=opt, metrics=[f1_m, AUC(), Precision()])
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
    pre_predictions = pd.Series(index = X.index, dtype='float64') # Series to add the predictions from prelim models testing
    for train, test in skf.split(X, y):
        X_train = X.iloc[train]
        X_test = X.iloc[test]
        y_train = y.iloc[train]
        gb = GradientBoostingClassifier(learning_rate=.01, n_estimators=90, min_samples_leaf=6 , min_samples_split=4 ,max_features= 3,max_depth= 5,subsample= .6)
        gb.fit(X_train, y_train)
        pred = gb.predict_proba(X_test)[:,1]
        pre_predictions.iloc[test] = pred 

    X['prediction'] = pre_predictions 

    for train, test in skf.split(X, y):


        model = create_baseline()
        es = EarlyStopping(monitor='loss', mode='min', verbose=0, patience=5)
        # Fit the model
        model.fit(X.iloc[train], y.iloc[train], verbose=0, epochs=500, batch_size=30, callbacks=[es])
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
