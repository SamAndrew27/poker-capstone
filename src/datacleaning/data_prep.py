import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np 

# splits tournaments from cash game
def get_tournaments(df):
    tourn_mask = df['cash_or_tourn'] == 'Holdem NL'        
    return df[tourn_mask]
    

def get_cash(df): # splits cash from tournament data
    cash_mask = df['cash_or_tourn'] != 'Holdem NL'
    return df[cash_mask]


def put_in_money(df): # seperates tournaments where I put in $ versus tournaeents were I didn't
    mask = df['money_beyond_blind'] == 1
    return df[mask]

def holdout_and_primary_tournaments(): # splits data into training/holdout
    df = pd.read_csv('/home/sam/Documents/DSI/capstone/poker/data/updated_DF.csv')
    df = get_tournaments(df)
    df = put_in_money(df)
    df = df.dropna(subset = ['position', 'BB_in_stack'])
    
    primary, holdout = train_test_split(df, test_size = .2)

    primary.to_csv('train_tournaments.csv')
    holdout.to_csv('holdout_tournaments.csv')
    



if __name__ == "__main__":
    pass 