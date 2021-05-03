import seaborn as sns 
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
plt.style.use('ggplot')


def read_in_holdout_return_X_y(remove_columns=True):
    """read in holdout data and split into X & y

    Args:
        remove_columns (bool, optional): If true remove unused columns and reorder. Defaults to True.

    Returns:
        2 arrays: X:features, y:target
    """    
    X = pd.read_csv('../../data/holdout_classification_tournaments_4-25.csv')
    X = X.drop(X.columns[0], axis = 1)
    y = X['made_or_lost']
    if remove_columns:
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




def read_in_training_return_Xy(remove_columns=True):
    """Read in training and split into X and y 

    Args:
        remove_columns (bool, optional): If true remove unused columns and put columns into correct order. Defaults to True.

    Returns:
        2 arrays: X:features, y:target 
    """    
    X = pd.read_csv('../../data/train_classification_tournaments_4-25.csv')
    X = X.drop(X.columns[0], axis = 1)
    y = X['made_or_lost']

    if remove_columns:
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



def join_training_holdout(target=False, remove_columns=True):
    """gets training and holdout data and joins them, returning either entire dataset or 2 arrays, features & targets

    Args:
        target (bool, optional): If true returns X. Defaults to False.
        remove_columns (bool, optional): If true remove unused columns and order used columns. Defaults to True.

    Returns:
        array(s): Either all the data available or X & y, X being array of features and y being the target variable 
    """    
    X, y = read_in_training_return_Xy(remove_columns=remove_columns)
    X_hold, y_hold = read_in_holdout_return_X_y(remove_columns=remove_columns)
    X['made_or_lost'] = y
    X_hold['made_or_lost'] = y_hold

    total_df = pd.concat([X, X_hold], ignore_index=True)

    if target:
        X = total_df
        y = X['made_or_lost']
        del X['made_or_lost']
        return X, y 
    else:

        return total_df
    
def split_won_lost():
    """Splits rows of hands won from rows of hands lost

    Returns:
        won: array of hands won 
        lost: array of hands lost
        df: entirety of won & lost 
    """    

    df = join_training_holdout()

    won_mask = df['made_or_lost'] == 1
    won = df[won_mask]
    lost_mask = df['made_or_lost'] == 0
    lost = df[lost_mask]
    return won, lost, df



def won_lost_for_BB(rounded = None, cutoff=200):
    """Won lost specific for BB visuals. Rounded determines degree of rounding Cutoff dictates max BB value considered.

    Args:
        rounded (float, optional): Number to round to (e.g. if 5 is input values will be rounded to nearest 5). Defaults to None, leading to no rounding
        cutoff (int, optional): max value of BB_in_stack. Defaults to 200.

    Returns:
        won: array of hands won 
        lost: array of hands lost
        df: entirety of won & lost 
    """    

    _, _, df = split_won_lost()

    if rounded != None:
        df['BB_in_stack'] = df['BB_in_stack'].apply(lambda x: rounded * round(x / rounded))
    
    mask = df['BB_in_stack'] <= cutoff
    df = df[mask]
    won_mask = df['made_or_lost'] == 1
    won = df[won_mask]
    lost_mask = df['made_or_lost'] == 0
    lost = df[lost_mask]

    return won, lost, df





def won_lost_for_num_players():
    """Won lost specific to num_players_before. rounds 'num_players_before' values over 2 down to 2

    Returns:
        won: array of hands won 
        lost: array of hands lost
        df: entirety of won & lost 
    """    
    _, _, df = split_won_lost()
    df['num_players_before'] = df['num_players_before'].apply(lambda x: round_down_num_players(x))
    won_mask = df['made_or_lost'] == 1
    won = df[won_mask]
    lost_mask = df['made_or_lost'] == 0
    lost = df[lost_mask]
    return won, lost, df

def round_down_num_players(x):
    """does rounding in 'won_lost_for_num_players' apply function

    Args:
        x ('num_players_before'): num players before column, values are ints

    Returns:
        int: either the existing value or 2 if value is over 2 
    """    
    if x >= 2:
        return 2
    else:
        return x






if __name__== "__main__":
    print(join_training_holdout().info())

