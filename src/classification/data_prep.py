import pandas as pd 
import numpy as np 
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV, train_test_split, KFold
from sklearn.metrics import f1_score, confusion_matrix, accuracy_score, recall_score, precision_score



def read_in_training_data(filename='train_classification_tournaments_4-25'):
    """retreives data from training csv and drops first column (which is just a double index)

    Args:
        filename (str, optional): filename of csv being read from. Defaults to 'train_classification_tournaments_4-25'.

    Returns:
        DataFrame: returns pandas dataframe from csv
    """    

    df = pd.read_csv(f'../../data/{filename}.csv')
    df = df.drop(df.columns[0], axis = 1)

    return df

def training_data_Xy(subset = True, scale=False, filename='train_classification_tournaments_4-25'):
    """reads in training data and splits into X & y
    Args:
        subset (bool, optional): If True removes unused columns. Defaults to True.
        scale (bool, optional): If true scales features (X data). Defaults to False.
        filename (str, optional): filename of csv being read from. Defaults to 'train_classification_tournaments_4-25'.


    Returns:
        X: features DataFrame
        y: target DataFrame (or series?)
    """    

    X = read_in_training_data(filename=filename)
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


def read_in_holdout_Xy(subset=True, filename='holdout_classification_tournaments_4-25'):
    """Reads in hold out data and splits into X & y

    Args:
        subset (bool, optional): If True removes unused columns. Defaults to True.
        filename(str, optional): Filename of holdout data. assumes data is held in same location as my own. Defaults to 'holdout_classification_tournaments_4-25'

    Returns:
        X, y: features,targets
    """    

    X = pd.read_csv(f'../../data/{filename}.csv')
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

def get_data_and_join(subset=True, training_filename='train_classification_tournaments_4-25', holdout_filename='holdout_classification_tournaments_4-25'):
    """Reads in Training / Holdout data and joints the two dataframes, and then splits them into X & y

    Args:
        subset (bool, optional): Whether to remove unused columns in DataFrames. Defaults to True.
        training_filename (str, optional): filename for training data. Defaults to 'train_classification_tournaments_4-25'.
        holdout_filename (str, optional): filename for holdout data. Defaults to 'holdout_classification_tournaments_4-25'.

    Returns:
        [type]: [description]
    """    
    X_training, y_training = training_data_Xy(subset, filename=training_filename)
    X_hold, y_hold = read_in_holdout_Xy(subset, filename=holdout_filename)

    X_training['made_or_lost'] = y_training
    X_hold['made_or_lost'] = y_hold
    all_data = pd.concat([X_training, X_hold], ignore_index=True)

    y = all_data['made_or_lost']
    X = all_data.drop(['made_or_lost'], axis=1)

    return X, y 


if __name__=="__main__":
    X, y = training_data_Xy()
    print(X.info())