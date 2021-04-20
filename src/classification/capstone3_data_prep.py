import pandas as pd 
import numpy as np 
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV, train_test_split, KFold
from sklearn.metrics import f1_score, confusion_matrix, accuracy_score, recall_score, precision_score

def read_in_data():
    df = pd.read_csv('/home/sam/Documents/DSI/capstone/poker/data/train_classification_tournaments.csv')
    df = df.drop(df.columns[0], axis = 1)

    return df


def read_in_return_Xy_no_unused():
    X = read_in_data()
    y = X['made_or_lost']

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

    return X, y 

def read_in_return_Xy_scaled_no_unused():
    X = read_in_data()
    y = X['made_or_lost']

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
            
    SS = StandardScaler()
    X = pd.DataFrame(data = SS.fit_transform(X), columns = list(X.columns))  

    return X, y 