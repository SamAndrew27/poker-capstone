from data_prep import read_in_and_split
import pandas as pd 
from itertools import combinations 
X_train, X_test, y_train, y_test  = read_in_and_split()
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
import xgboost as xg 
from sklearn.neighbors import KNeighborsRegressor



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

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .2, random_state=127)

    col_lst = column_combinations()

    model_lst = [RandomForestRegressor(), ]
if __name__ == "__main__":

