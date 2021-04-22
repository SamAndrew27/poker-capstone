import seaborn as sns 
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
plt.style.use('ggplot')


def load_whole():
    '''
    change this to entire dataframe eventually 
    '''
    df = pd.read_csv('../../data/train_classification_tournaments.csv')
    df = df.drop(df.columns[0], axis = 1)
    won_mask = df['made_or_lost'] == 1
    won = df[won_mask]
    lost_mask = df['made_or_lost'] == 0
    lost = df[lost_mask]
    return won, lost, df


def won_lost_for_BB(rounded = None, cutoff=200):
    _, _, df = load_whole()

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
    _, _, df = load_whole()
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
    won, lost, df = load_whole()
    print(df.info())