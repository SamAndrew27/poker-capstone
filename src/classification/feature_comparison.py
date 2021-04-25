import pandas as pd 
from sklearn.model_selection import cross_val_score
from itertools import combinations 
import numpy as np 
# from class_prep import read_in_return_X_scaled, read_in_return_X_scaled_no_time

from data_prep import read_in_return_Xy_scaled_no_unused, read_in_return_Xy_all_columns
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier 
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import RidgeClassifier, LogisticRegression
from sklearn.model_selection import KFold
from sklearn.metrics import brier_score_loss, roc_auc_score

xgb = XGBClassifier()

def column_combinations(base_list, considered_columns, r=[1]): # all possible combinations of columns (that we are considering)
    """Creates a list of lists. list contain combinations of column names

    Args:
        base_list (list): columns to always be included
        considered_columns (list): columns to be fluctuated through
        r (list, optional): Number of column combinations. see itertools documentation. it is 'r' in the combinations function. Defaults to [1].

    Returns:
        list of lists: columns to be tested 
    """    
    column_list = []
    # base_list = ['suited','low_card','position','high_card','card_rank','limpers', 'raises&reraises','num_players_before', 'num_players_after','BB_in_stack'] # list of stuff that will always be there
    column_list.append(base_list)
    # considered_columns = ['total_actions_witnessed_relevant_players','vpip_relavant_players', 'weighted_relevant_vpip', 'buyin'] # list of stuff that won't always be there # , , , , 

    for num in r:
        subset = list(combinations(considered_columns, num))
        for cols in subset:
            temp = base_list.copy()
            for col in cols:
                temp.append(col)
            column_list.append(temp)

    return column_list


def cv(model, X, y):
    """performs cv and gets mean scores

    Args:
        model: model to use sklearn cv on 
        X (array): features
        y (array): target

    Returns:
        2 floats: mearn roc, mean brier
    """    
    roc_auc = cross_val_score(model, X, y, n_jobs = -1, scoring= 'roc_auc')
    brier = cross_val_score(model, X, y, n_jobs = -1, scoring= 'neg_brier_score')

    return np.mean(roc_auc), -np.mean(brier)



# def test_different_models_sans_XGB_Ridge():

#     X, y = read_in_return_Xy_scaled_no_unused()


#     result = pd.DataFrame(columns=['model', 'columns', 'brier', 'roc_auc']) 

#     col_lst = column_combinations()
#     model_dic = {0:'RandomForest' , 1: 'GradientBoost', 2: 'AdaBoost', 3:'KNN', 4: 'logistic'}
#     model_lst = [RandomForestClassifier(), GradientBoostingClassifier(), AdaBoostClassifier(), KNeighborsClassifier(), LogisticRegression()]
#     count = 0
#     for idx, model in enumerate(model_lst):
#         print(idx)
#         for cols in col_lst:
#             X_subset = X[cols]
#             X_cols = list(X_subset.columns)
#             roc_auc, brier = cv(model, X_subset, y)

#             # X_cols.remove('buyin')# removing columns for ease of reading results
#             X_cols.remove('suited')  
#             X_cols.remove('position')
#             X_cols.remove('card_rank')
#             X_cols.remove('low_card')
#             X_cols.remove('high_card')
#             X_cols.remove('BB_in_stack')
#             X_cols.remove('limpers')
#             X_cols.remove('raises&reraises')
#             X_cols.remove('num_players_before')
#             X_cols.remove('num_players_after')
#             # X_cols.remove('total_actions_witnessed_relevant_players')
#             # X_cols.remove('vpip_relavant_players')

#             result.loc[count] = [model_dic[idx], X_cols, brier, roc_auc] # can i index like this? 
#             count += 1

#     return result 



def test_different_models_sans_XGB_Ridge_scale_within(base_list, considered_columns, r=[1]):
    """tests feature combinations w/ sklearn cv to get brier/roc scores

    Args:
        base_list (list of columns to be considered): list of columns to always be included
        considered_columns ([type]): [description]

    Returns:
        [type]: [description]
    """    

    X, y = read_in_return_Xy_all_columns()


    result = pd.DataFrame(columns=['model', 'columns', 'brier', 'roc_auc']) 

    col_lst = column_combinations(base_list, considered_columns, r)
    model_dic = {0:'RandomForest' , 1: 'GradientBoost', 2: 'AdaBoost', 3:'KNN', 4: 'logistic'}
    model_lst = [RandomForestClassifier(), GradientBoostingClassifier(), AdaBoostClassifier(), KNeighborsClassifier(), LogisticRegression()]
    count = 0
    for idx, model in enumerate(model_lst):
        print(idx)
        for cols in col_lst:
            X_subset = X[cols]
            X_cols = list(X_subset.columns)
            SS = StandardScaler()
            X_subset = pd.DataFrame(data=SS.fit_transform(X_subset), columns = X_cols)

            roc_auc, brier = cv(model, X_subset, y)

            for col in base_list:
                X_cols.remove(col)  


            result.loc[count] = [model_dic[idx], X_cols, brier, roc_auc] # can i index like this? 
            count += 1

    return result 

if __name__ == "__main__":

    result = test_different_models_sans_XGB_Ridge_scale_within(base_list=['BB_in_stack', 'suited','position','raises&reraises','num_players_before', 'num_players_after','card_rank'], considered_columns = ['limpers', 'low_card','high_card'], r=[1,2,3])

    # result.to_csv('../../data/classification_compare_limpers_low_high_card.csv')

    # X, y = read_in_return_Xy_all_columns()
    # result = column_combinations(base_list=['suited','low_card','position','high_card','card_rank', 'raises&reraises','num_players_before', 'num_players_after','BB_in_stack'], considered_columns = ['limpers', 'callers', 'limps&calls'])
    # for cols in result:
    #     X_subset = X[cols]
    #     print(X_subset.info())
    # maybe get rid of buyin?
    # maybe get rid of position?