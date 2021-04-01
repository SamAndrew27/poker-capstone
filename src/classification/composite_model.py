from class_prep import read_in_return_Xy_no_time
from sklearn.ensemble import GradientBoostingClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
import pandas as pd 
import numpy as np 
from sklearn.model_selection import KFold

def composite_model(X, y, primary_model, preliminary_model1, preliminary_model2, num_folds=5): # primary model does the final regression, preliminary produces prediction for primary to factor in

    kf = KFold(n_splits=num_folds, shuffle=True)
    error = np.empty(num_folds)
    index = 0
    pre_predictions1 = pd.Series(index = X.index) # Series to add the predictions from prelim models testing
    pre_predictions2 = pd.Series(index = X.index)

    for train, test in kf.split(X):
        X_train = X.iloc[train]
        X_test = X.iloc[test]
        y_train = y.iloc[train]


        preliminary_model1.fit(X_train, y_train) # running through both models and adding to respective series

        prediction1 = preliminary_model1.predict_proba(X_test) 
        prediction1 = prediction1[:,0]
        pre_predictions1.iloc[test] = prediction1


        preliminary_model2.fit(X_train, y_train) 
        predictions2 = preliminary_model2.predict_proba(X_test) 
        predictions2 = predictions2[:,0]

        pre_predictions2.iloc[test] = predictions2



    X['prediction1'] = pre_predictions1 # add series to dataframe as columns
    X['prediction2'] = pre_predictions2


    for train, test in kf.split(X):
        X_train = X.iloc[train]
        X_test = X.iloc[test]
        y_train = y.iloc[train]
        y_test = y.iloc[test]        

        primary_model.fit(X_train, y_train)
        final_prediction = primary_model.predict_proba(X_test) # get prediction

        error[index] = f1_score(y_test,final_prediction) # look at r2 score 
        index += 1


    return np.mean(error)

ada = AdaBoostClassifier(learning_rate=.021, n_estimators= 119)

logistic = LogisticRegression(l1_ratio=.075, max_iter=5000, penalty='elasticnet', solver='saga')

grad_boost = GradientBoostingClassifier(learning_rate=.042, max_depth=2, max_features=2, min_samples_leaf=9, min_samples_split=6, n_estimators=37, subsample=.3)

if __name__ == "__main__":
    X, y = read_in_return_Xy_no_time()

    print(composite_model(X, y, grad_boost, logistic, ada, num_folds=5))
    

