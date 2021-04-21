import pandas as pd 
from sklearn.model_selection import cross_val_score
from itertools import combinations 
import numpy as np 
from class_prep import read_in_return_X_scaled, read_in_return_X_scaled_no_time

from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier 
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import RidgeClassifier, LogisticRegression
from sklearn.model_selection import KFold
from sklearn.metrics import brier_score_loss, roc_auc_score

def column_combinations(): # all possible combinations of columns (that we are considering)
    column_list = []
    base_list = ['buyin', 'BB_in_stack', 'total_players', 'position', 'suited',  'low_card','high_card','card_rank','limpers', 'raises&reraises','num_players_before', 'num_players_after','vpip_relavant_players','total_actions_witnessed_relevant_players'] # list of stuff that will always be there
    column_list.append(base_list)
    time_columns = ['amount_to_call','callers'] # list of stuff that won't always be there # , , , , 
    r = [1,2] # number of possible combinations

    for num in r:
        subset = list(combinations(time_columns, num))
        for cols in subset:
            temp = base_list.copy()
            for col in cols:
                temp.append(col)
            column_list.append(temp)

    return column_list


def cv(model, X, y):
    roc_auc = cross_val_score(model, X, y, n_jobs = -1, scoring= 'roc_auc')
    brier = cross_val_score(model, X, y, n_jobs = -1, scoring= 'neg_brier_score')

    return np.mean(roc_auc), -np.mean(brier)





# saving this for now, going to try again w/o the problem causing models
def test_different_models():

    X, y = read_in_return_X_scaled_no_time()

    result = pd.DataFrame(columns=['model', 'columns', 'brier', 'roc_auc']) 

    col_lst = column_combinations()
    model_dic = {0:'XGB', 1:'RandomForest' , 2: 'GradientBoost', 3: 'AdaBoost', 4:'KNN', 5:'Ridge', 6: 'logistic'}
    model_lst = [XGBClassifier(), RandomForestClassifier(), GradientBoostingClassifier(), AdaBoostClassifier(), KNeighborsClassifier(), RidgeClassifier(), LogisticRegression()]
    count = 0

    for idx, model in enumerate(model_lst):
        for cols in col_lst:
            X_subset = X[cols]
            X_cols = list(X_subset.columns)
            roc_auc, brier = cv(model, X_subset, y)

            X_cols.remove('buyin')# removing columns for ease of reading results
            X_cols.remove('suited')  
            X_cols.remove('position')
            X_cols.remove('total_players')
            X_cols.remove('card_rank')
            X_cols.remove('low_card')
            X_cols.remove('high_card')
            X_cols.remove('BB_in_stack')



            result.loc[count] = [model_dic[idx], X_cols, brier, roc_auc] # can i index like this? 
            count += 1

    return result 

# just discluding XGB, documentation is making me lose my mind
# after running 6 different times, Gradient is always best
# Logistic is always best at brier
# Adaboost is always best at ROCAUC
# going to focus on turning Gradient
# then Logistic/Adaboost and consider a composite model 

def test_different_models_sans_XGB_Ridge():

    X, y = read_in_return_X_scaled()


    result = pd.DataFrame(columns=['model', 'columns', 'brier', 'roc_auc']) 

    col_lst = column_combinations()
    model_dic = {0:'RandomForest' , 1: 'GradientBoost', 2: 'AdaBoost', 3:'KNN', 4: 'logistic'}
    model_lst = [RandomForestClassifier(), GradientBoostingClassifier(), AdaBoostClassifier(), KNeighborsClassifier(), LogisticRegression()]
    count = 0
    for idx, model in enumerate(model_lst):
        print(idx)
        for cols in col_lst:
            X_subset = X[cols]
            X_cols = list(X_subset.columns)
            roc_auc, brier = cv(model, X_subset, y)

            X_cols.remove('buyin')# removing columns for ease of reading results
            X_cols.remove('suited')  
            X_cols.remove('position')
            X_cols.remove('total_players')
            X_cols.remove('card_rank')
            X_cols.remove('low_card')
            X_cols.remove('high_card')
            X_cols.remove('BB_in_stack')
            X_cols.remove('limpers')
            X_cols.remove('raises&reraises')
            X_cols.remove('num_players_before')
            X_cols.remove('num_players_after')
            X_cols.remove('total_actions_witnessed_relevant_players')
            X_cols.remove('vpip_relavant_players')

            result.loc[count] = [model_dic[idx], X_cols, brier, roc_auc] # can i index like this? 
            count += 1

    return result 





# table this for now. return if you have the time - might be too tired to do this as an evening project
# instead ran above 5 different times
def test_different_models_Kfolds_method():

    X, y = read_in_return_X_scaled()


    result = pd.DataFrame(columns=['model', 'columns', 'brier', 'roc_auc']) 
    # X_test = SS.transform(X_train) # pretty sure I should use CV to compare models, not the testing data
    # y_test = np.log(y_test)
    col_lst = column_combinations()
    model_dic = {0:'RandomForest' , 1: 'GradientBoost', 2: 'AdaBoost', 3:'KNN', 4: 'logistic'}
    model_lst = [RandomForestClassifier(), GradientBoostingClassifier(), AdaBoostClassifier(), KNeighborsClassifier(), LogisticRegression()]
    count = 0
    
    kf = KFold(n_splits=10, shuffle = True)
    error = np.empty(10)
    
    for train, test in kf.split(X):
        for idx, model in enumerate(model_lst):
            for cols in col_lst:
                X_subset = X[cols]
                X_train = X_subset.iloc[train]
                X_test = X_subset.iloc[test]
                y_train = y.iloc[train]
                y_test = y.iloc[test]
                
                X_cols = list(X_subset.columns)
                

                X_cols.remove('buyin')# removing columns for ease of reading results
                X_cols.remove('suited')  
                X_cols.remove('position')
                X_cols.remove('total_players')
                X_cols.remove('card_rank')
                X_cols.remove('low_card')
                X_cols.remove('high_card')
                X_cols.remove('BB_in_stack')

                model.fit(X_train, y_train)

                result.loc[count] = [model_dic[idx], X_cols, brier, roc_auc] # can i index like this? 
                count += 1

    return result 

def test_XGB_gradient_ADA():

    X, y = read_in_return_X_scaled_no_time()
    X = X[['buyin', 'BB_in_stack', 'total_players', 'position', 'suited',  'low_card','high_card','card_rank','limpers', 'raises&reraises','num_players_before', 'num_players_after','vpip_relavant_players','total_actions_witnessed_relevant_players']]

    result = pd.DataFrame(columns=['model', 'brier', 'roc_auc'], index = list(range(3))) 
    model_dic = {0:'XGB', 1: 'GradientBoost', 2: 'AdaBoost'}
    model_lst = [XGBClassifier(), GradientBoostingClassifier(), AdaBoostClassifier()]
    kf = KFold(n_splits=10, shuffle = True)

    brier_xgb = []
    roc_xgb = []
    brier_gradient = []
    roc_gradient = []
    brier_ada = []
    roc_ada = []
       

    for train, test in kf.split(X):
        for idx, model in enumerate(model_lst):
            roc_auc, brier = cv(model, X, y)

            X_train = X.iloc[train]
            X_test = X.iloc[test]
            y_train = y.iloc[train]
            y_test = y.iloc[test]        
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            brier = brier_score_loss(y_test, y_pred)
            roc_auc = roc_auc_score(y_test, y_pred)

            if idx == 0:
                brier_xgb.append(brier)
                roc_xgb.append(roc_auc)
            if idx == 1:
                brier_gradient.append(brier)
                roc_gradient.append(roc_auc)
            if idx == 2:
                brier_ada.append(brier)
                roc_ada.append(roc_auc)         

    result.loc[0] = [model_dic[0], np.mean(brier_xgb), np.mean(roc_xgb)] 
    result.loc[1] = [model_dic[1], np.mean(brier_gradient), np.mean(roc_gradient)] 
    result.loc[2] = [model_dic[2], np.mean(brier_ada), np.mean(roc_ada)] 

    return result 




if __name__ == "__main__":

    result = test_XGB_gradient_ADA()

    result.to_csv('../../data/classification_model_compare_XGB.csv')


    # maybe include 'callers'? seems to have a small impact maybe?
    # same for 'amount_to_call'
    # 'average_table_vpip', 'total_actions_witnessed' appeared to have very little impact 