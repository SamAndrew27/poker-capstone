from data_prep import read_in_and_split, read_in_return_Xy
import pandas as pd 
import numpy as np
from itertools import combinations 
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from xgboost import XGBRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import Ridge, Lasso
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import  cross_val_score
import matplotlib.pyplot as plt

def column_combinations(): # all possible combinations of columns (that we are considering)
    column_list = []
    base_list = ['buyin', 'total_players', 'position', 'suited',  'low_card','high_card','card_rank'] # list of stuff that will always be there
    column_list.append(base_list)
    time_columns = ['hour','days_since_start', 'hand_frequency'] # list of stuff that won't always be there
    r = [1,2,3] # number of possible combinations

    for num in r:
        subset = list(combinations(time_columns, num))
        for cols in subset:
            temp = base_list.copy()
            for col in cols:
                temp.append(col)
            column_list.append(temp)

    return column_list

def test_different_models():

    X, y = read_in_return_Xy()
    SS = StandardScaler()
    X_total_cols = list(X.columns)
    X = pd.DataFrame(data = SS.fit_transform(X), columns = X_total_cols)
    y = y.apply(lambda x: np.log(x + 1))

    result = pd.DataFrame(columns=['model', 'columns', 'r2', 'r2_adjusted']) 
    # X_test = SS.transform(X_train) # pretty sure I should use CV to compare models, not the testing data
    # y_test = np.log(y_test)
    col_lst = column_combinations()

    model_lst = [XGBRegressor(), RandomForestRegressor(), GradientBoostingRegressor(), AdaBoostRegressor(), KNeighborsRegressor(), Ridge(), Lasso()]
    count = 0
    for idx, model in enumerate(model_lst):
        for cols in col_lst:
            X_subset = X[cols]
            X_cols = list(X_subset.columns)
            r2 = cv(model, X_subset, y)
            adjusted = 1 - (1-r2) * ((len(y) - 1) / (len(y) - len(X_cols) -1  )) # r2 adjusted
            result.loc[count] = [idx, cols, r2, adjusted] # can i index like this? 
            count += 1

    return result 


def cv(model, X, y):
    r2_score = cross_val_score(model, X, y, n_jobs = -1, scoring= 'r2')
    return np.mean(r2_score) 

if __name__ == "__main__":
    results = test_different_models()
    results.to_csv('model_comparison.csv')


    # X, y = read_in_return_Xy()
    # print(y.iloc[0:10])
    # y = y.apply(lambda x: np.log(x + 1))
    # print(y.iloc[0:10])
