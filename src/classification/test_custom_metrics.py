from tensorflow.keras import backend as K 
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import StratifiedKFold
from capstone3_data_prep import read_in_return_Xy_scaled_no_unused

def model_eval(model, X, y):
    skf = StratifiedKFold(n_splits=5, shuffle=True)
    cvscores = []
    for train, test in skf.split(X, y):

        model.fit(X.iloc[train], y.iloc[train])
        # evaluate the model
        y_pred = model.predict(X.iloc[test])
        cvscores.append(f1_m(y.iloc[test], y_pred))
    print("%.2f%% (+/- %.2f%%)" % (np.mean(cvscores), np.std(cvscores)))


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


if __name__=="__main__":

    gb_final = GradientBoostingClassifier(learning_rate=.01, n_estimators=90, min_samples_leaf=6 , min_samples_split=4 ,max_features= 3,max_depth= 5,subsample= .6)
    X, y = read_in_return_Xy_scaled_no_unused()
    model_eval(gb_final, X, y)