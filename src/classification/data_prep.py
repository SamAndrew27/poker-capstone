import pandas as pd 
import numpy as np 
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV, train_test_split, KFold
from sklearn.metrics import f1_score, confusion_matrix, accuracy_score, recall_score, precision_score

# CHANGING NAMES AROUND, FIX IN OTHER SCRIPTS!!!!!


def read_in_training_data():
    """retreives data

    Returns:
        DataFrame: returns pandas dataframe from csv
    """    
    df = pd.read_csv('../../data/train_classification_tournaments_4-25.csv')
    df = df.drop(df.columns[0], axis = 1)

    return df

def training_data_Xy(subset = True, scale=False):

    X = read_in_training_data()
    y = X['made_or_lost']

    if subset:
        X =  X[['suited',
                'low_card',
                'position',
                'high_card',
                'card_rank',
                'limpers', 
                'raises&reraises',
                'num_players_before',
                'num_players_after',
                'BB_in_stack']]
    else:
        del X['made_or_lost']

    if scale:
        SS = StandardScaler()
        X = pd.DataFrame(data = SS.fit_transform(X), columns = list(X.columns))  

    return X, y


# should probably delete this function
# def read_in_return_Xy_scaled_no_unused():

#     X = read_in_data()
#     y = X['made_or_lost']

#     X =  X[['suited',
#             'low_card',
#             'position',
#             'high_card',
#             'card_rank',
#             'limpers', 
#             'raises&reraises',
#             'num_players_before',
#             'num_players_after',
#             'BB_in_stack']]
            
#     SS = StandardScaler()
#     X = pd.DataFrame(data = SS.fit_transform(X), columns = list(X.columns))  

#     return X, y 

# def read_in_return_Xy_all_columns():
#     """Reads in X & y w/ no feature removal

#     Returns:
#         X,y: features, target
#     """    
#     X = read_in_data()
#     y = X['made_or_lost']

#     del X['made_or_lost']

#     return X, y 

def read_in_holdout_Xy(subset=True):
    """Reads in hold out data and leaves just relevant columns 

    Returns:
        X, y: features,targets
    """    
    X = pd.read_csv('../../data/holdout_classification_tournaments_4-25.csv')
    X = X.drop(X.columns[0], axis = 1)
    y = X['made_or_lost']
    if subset:
        X =  X[['suited',
                'low_card',
                'position',
                'high_card',
                'card_rank',
                'limpers', 
                'raises&reraises',
                'num_players_before',
                'num_players_after',
                'BB_in_stack']]
    else:
        del X['made_or_lost']

    return X, y 




if __name__=="__main__":
    X, y = read_in_return_Xy_no_unused()
    print(X.info())