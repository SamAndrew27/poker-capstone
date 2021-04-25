from xgboost import XGBClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score, brier_score_loss 
from sklearn.model_selection import StratifiedKFold
from data_prep import read_in_return_Xy_scaled_no_unused
import pandas as pd 
import numpy as np 

# load data
X, y = read_in_return_Xy_scaled_no_unused()

def compare_gradient_xg_boost(X,y):
    gb = GradientBoostingClassifier()
    xgb = XGBClassifier()

    gb_roc_results = []
    gb_brier_results = []
    xgb_roc_results = []
    xgb_brier_results = []

    skf = StratifiedKFold(n_splits=10, shuffle=True)

    for train, test in skf.split(X,y):
        X_train = X.iloc[train]
        y_train = y.iloc[train]
        X_test = X.iloc[test]
        y_test = X.iloc[test]

        gb.fit(X_train,y_train)
        xgb.fit(X_train,y_train)
        gb_predictions = gb.predict(X_test)
        xgb_pre_dictions = xgb.predict(X_test)
        # xgb_predictions = [round(value) for value in xgb_pre_dictions]

        gb_roc_auc = roc_auc_score(y_test, gb_predictions)
        gb_brier = brier_score_loss(y_test, gb_predictions)
        xgb_roc_auc = roc_auc_score(y_test, xgb_predictions)
        xgb_brier = brier_score_loss(y_test, xgb_predictions)

        gb_roc_results.append(gb_roc_auc)
        gb_brier_results.append(gb_brier)
        xgb_roc_results.append(xgb_roc_auc)
        xgb_brier_results.append(xgb_brier)
    
    print(f'GB  Brier:{np.mean(gb_brier_results)}')
    print(f'XGB Brier:{np.mean(gb_brier_results)}')
    print(f'GB  ROC_AUC:{np.mean(gb_brier_results)}')
    print(f'XGB ROC_AUC:{np.mean(gb_brier_results)}')








if __name__=="__main__":
    # compare_gradient_xg_boost(X,y)
    xgb = XGBClassifier()
    xgb.fit(X,y)
    result = xgb.predict(X)
    for elem in result:
        print(elem)
        print(type(elem))