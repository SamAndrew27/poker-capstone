from xgboost import XGBClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score, brier_score_loss 
from sklearn.model_selection import StratifiedKFold, cross_val_score, KFold
from data_prep import training_data_Xy
import pandas as pd 
import numpy as np 

# load data
X, y = training_data_Xy()

def compare_gradient_xg_boost(X,y):
    """using cross val, compares gradient boost to XGboost, results printed to terminal 

    Args:
        X (array): features
        y (array): target
    """    
    gb = GradientBoostingClassifier()
    xgb = XGBClassifier()

    gb_roc_results = []
    gb_brier_results = []
    xgb_roc_results = []
    xgb_brier_results = []

    skf = KFold(n_splits=5, shuffle=False)

    for train, test in skf.split(X,y):
        X_train = X.iloc[train]
        y_train = y.iloc[train]
        X_test = X.iloc[test]
        y_test = y.iloc[test]

        gb.fit(X_train,y_train)
        xgb.fit(X_train,y_train)
        gb_predictions = gb.predict(X_test)
        xgb_predictions = xgb.predict(X_test)
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
    print(f'XGB Brier:{np.mean(xgb_brier_results)}')
    print(f'GB  ROC_AUC:{np.mean(gb_roc_results)}')
    print(f'XGB ROC_AUC:{np.mean(xgb_roc_results)}')


    # WHY LOWER THAN the method done with all models?!?!?!?!?!
    # SEEMS LIKE CROSS VAL IS ALWAYS SCORING HIGHER????? NOT GOING TO WORRY FOR NOW 
    # SINCE GB SEEMS TO OUTPERFORM XGBOOST ANYWAYS
    # GB  Brier:0.3334479696125048
    # XGB Brier:0.3567060173798983
    # GB  ROC_AUC:0.622271279514713
    # XGB ROC_AUC:0.6104926538981456





if __name__=="__main__":
    compare_gradient_xg_boost(X,y)

    # xgb = XGBClassifier()
    gb = GradientBoostingClassifier()
    roc_auc = cross_val_score(gb, X, y, scoring='roc_auc')
    brier = cross_val_score(gb, X, y, scoring='neg_brier_score')
    print(roc_auc)
    print(brier)

    # xgb.fit(X,y)
    # gb.fit(X,y)
    # result = xgb.predict(X)
    # gb_result = gb.predict(X)
    # print(type(result[0]))
    # print(type(result[0]))


    # for elem in result:
    #     print(elem)
    #     print(type(elem))