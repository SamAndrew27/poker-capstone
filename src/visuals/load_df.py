import seaborn as sns 
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
plt.style.use('ggplot')


# CAN DEFINITELY COMBINE SOME OF THESE FUNCTIONS, SOME MAYBE TOTALLY UNECESSARY, OTHERS COULD BECOME A BOOL IN ANOTHER FUNCTION 


def read_in_holdout_return_X_y(remove_columns=True):
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



def join_training_holdout():
    X, y = read_in_training_return_Xy()
    X_hold, y_hold = read_in_holdout_return_X_y()
    X['made_or_lost'] = y
    X_hold['made_or_lost'] = y_hold

    total_df = pd.concat([X, X_hold], ignore_index=True)

    return total_df
    
def split_won_lost():
    '''
    change this to entire dataframe eventually 
    '''

    df = join_training_holdout()

    won_mask = df['made_or_lost'] == 1
    won = df[won_mask]
    lost_mask = df['made_or_lost'] == 0
    lost = df[lost_mask]
    return won, lost, df




def won_lost_for_BB(rounded = None, cutoff=200):
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
    _, _, df = split_won_lost()
    df['num_players_before'] = df['num_players_before'].apply(lambda x: round_down_num_players(x))
    won_mask = df['made_or_lost'] == 1
    won = df[won_mask]
    lost_mask = df['made_or_lost'] == 0
    lost = df[lost_mask]
    return won, lost, df

def round_down_num_players(x):
    if x >= 2:
        return 2
    else:
        return x






if __name__== "__main__":
    print(join_training_holdout().info())

