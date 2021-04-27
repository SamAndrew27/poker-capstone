from sklearn.linear_model import Ridge
from regression_prep import scaled_and_logged_X_y
from sklearn.metrics import r2_score
import numpy as np
import pandas as pd 
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import KFold, cross_val_score


# come back to this? get predictions on unseen data rather than data it was trained on? 
def cv_two_models(X, y, primary_model, preliminary_model, num_folds=5): # primary model does the final regression, secondary model produces prediction for primary to factor in

    kf = KFold(n_splits=num_folds, shuffle=True)
    error = np.empty(num_folds)
    index = 0
    
    for train, test in kf.split(X):
        X_train = X.iloc[train]
        X_test = X.iloc[test]
        y_train = y.iloc[train]
        y_test = y.iloc[test]


        preliminary_model.fit(X_train, y_train) 
        prelim_prediction_test = preliminary_model.predict(X_test) # get predictions of 1st model
        prelim_prediction_train = preliminary_model.predict(X_train) # get predictions of 1st model

        #X_train['preliminary_prediction'] = prelim_prediction # add it as a column to X
        X_test['preliminary_prediction'] = prelim_prediction_test
        X_train['preliminary_prediction'] = prelim_prediction_train

        primary_model.fit(X_train, y_train)
        final_prediction = primary_model.predict(X_test) # get prediction

        error[index] = r2_score(y_test,final_prediction) # look at r2 score 
        index += 1

    return np.mean(error)

def cv_two_models_round2(X, y, primary_model, preliminary_model, num_folds=5): # primary model does the final regression, secondary model produces prediction for primary to factor in

    kf = KFold(n_splits=num_folds, shuffle=True)
    error = np.empty(num_folds)
    index = 0
    pre_predictions = pd.Series(index = X.index) # Series to add the predictions from first models testing

    for train, test in kf.split(X):
        X_train = X.iloc[train]
        X_test = X.iloc[test]
        y_train = y.iloc[train]


        preliminary_model.fit(X_train, y_train) 
        prelim_prediction = preliminary_model.predict(X_test) # get predictions of 1st model

        #X_train['preliminary_prediction'] = prelim_prediction # add it as a column to X
        pre_predictions.iloc[test] = prelim_prediction


    X['preliminary_predictions'] = pre_predictions

    for train, test in kf.split(X):
        X_train = X.iloc[train]
        X_test = X.iloc[test]
        y_train = y.iloc[train]
        y_test = y.iloc[test]        

        primary_model.fit(X_train, y_train)
        final_prediction = primary_model.predict(X_test) # get prediction

        error[index] = r2_score(y_test,final_prediction) # look at r2 score 
        index += 1


    return np.mean(error)


if __name__ == "__main__":
    X, y = scaled_and_logged_X_y()
    gbr = GradientBoostingRegressor(learning_rate = .15, n_estimators = 50, max_depth=2, max_features=3, min_samples_split=10)
    en = Ridge(alpha=425, solver= 'sag')

    print(cv_two_models_round2(X, y, gbr, en))

    # kf = KFold(n_splits=2)
    # error = np.empty(2)
    # index = 0

    # for train, test in kf.split(X):
    #     en.fit(X.iloc[train], y.iloc[train])
    #     prelim_prediction = en.predict(X.iloc[test])
    #     print(prelim_prediction)