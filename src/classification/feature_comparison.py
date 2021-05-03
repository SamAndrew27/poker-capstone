from itertools import combinations 
import numpy as np 
import pandas as pd 
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier 
from sklearn.linear_model import RidgeClassifier, LogisticRegression
from sklearn.metrics import brier_score_loss, roc_auc_score
from sklearn.model_selection import cross_val_score, KFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

from data_prep import training_data_Xy


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
    column_list.append(base_list)

    for num in r: # gets column combination of sizes included in list 'r'
        subset = list(combinations(considered_columns, num))
        for cols in subset:
            temp = base_list.copy() 
            for col in cols: # adds columns from each considered column combination to copy of base_list
                temp.append(col)
            column_list.append(temp) # adds copy + combination to column_list

    return column_list


def cv(model, X, y):
    """performs cv and gets mean scores for roc_auc, brier

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



def test_different_models_scale_within(base_list, considered_columns, r=[1]):
    """tests feature combinations w/ sklearn cv to get brier/roc scores for each model, for each combination of columns
    base_list columns are always included. Will get every possible combination of 'considered_column' possible given values in 'r'
    for more details refer to 'column_combinations' function and the 'Combinations' function from itertools

    Args:
        base_list (list): columns to always be included in test
        considered_columns (list): columns that will possibly be included
        r (list, optional): Size of the combinations made with 'considered_columns'. Defaults to [1], meaning ever 'considered_column' will be included once

    Returns:
        DataFrame: Dataframe with 4 columns: the name of the model, the columns (besides the base columns) considered, brier score, roc auc score
    """    

    X, y = training_data_Xy(subset=False)


    result = pd.DataFrame(columns=['model', 'columns', 'brier', 'roc_auc']) 

    col_lst = column_combinations(base_list, considered_columns, r)
    model_dic = {0:'RandomForest' , 1: 'GradientBoost', 2: 'AdaBoost', 3:'KNN', 4: 'logistic'} # dictionary to get names of models
    model_lst = [RandomForestClassifier(), GradientBoostingClassifier(), AdaBoostClassifier(), KNeighborsClassifier(), LogisticRegression()] # models to be considered
    count = 0
    for idx, model in enumerate(model_lst): # iterate through model list
        print(idx)
        for cols in col_lst: # iterate through column list
            X_subset = X[cols] # reduces X to just columns that ought to be considered
            X_cols = list(X_subset.columns)
            SS = StandardScaler()
            X_subset = pd.DataFrame(data=SS.fit_transform(X_subset), columns = X_cols) # scales X

            roc_auc, brier = cv(model, X_subset, y) # get scores using cv function

            for col in base_list: # removes columns from base list from X_cols to remove extra info from DataFrame
                X_cols.remove(col)  


            result.loc[count] = [model_dic[idx], X_cols, brier, roc_auc] #inserting results into DataFrame
            count += 1

    return result 

if __name__ == "__main__":

    result = test_different_models_scale_within(base_list=['BB_in_stack', 'suited','position','raises&reraises','num_players_before', 'num_players_after','card_rank'], considered_columns = ['limpers', 'low_card','high_card'], r=[1,2,3])

    # result.to_csv('../../data/classification_compare_limpers_low_high_card.csv')

    # X, y = read_in_return_Xy_all_columns()
    # result = column_combinations(base_list=['suited','low_card','position','high_card','card_rank', 'raises&reraises','num_players_before', 'num_players_after','BB_in_stack'], considered_columns = ['limpers', 'callers', 'limps&calls'])
    # for cols in result:
    #     X_subset = X[cols]
    #     print(X_subset.info())
    # maybe get rid of buyin?
    # maybe get rid of position?






















# SHOULD PROBABLY JUST DELETE THIS CODE BUT COMPARE TO FUNCTION ABOVE FIRST
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