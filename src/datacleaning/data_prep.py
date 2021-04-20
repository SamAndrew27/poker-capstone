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

''' # used this for regression, ignore now. 
def holdout_and_primary_tournaments(): # splits data into training/holdout
    df = pd.read_csv('/home/sam/Documents/DSI/capstone/poker/data/updated_DF.csv')
    df = get_tournaments(df)
    df = put_in_money(df)
    df = df.dropna(subset = ['position', 'BB_in_stack'])
    
    primary, holdout = train_test_split(df, test_size = .2)

    primary.to_csv('train_tournaments.csv')
    holdout.to_csv('holdout_tournaments.csv')
'''

# includes removing columns used in the creation of other columns
# just removing everything that couldn't potentially be used for model building
# removing both gametypes... OOPS (one is the one i created, useful for delineating cash from tournaments)
# BUT CONSIDER LOOKING AT THE ONE THEY CREATED! and naming the one I created something else 
# will create smaller columns as necessary 
def remove_unused_columns(df, drop = False):
    if drop:
        df = df.drop(df.columns[0], axis = 1)

    result = df[['buyin','won', 'bet','made_money','BB', 'BB_in_stack','starting_stack','total_players','table_max_players', 'position', 
        'flop_bet', 'turn_bet','river_bet', 'preflop_bet', 'net_outcome', 'all_in', 'money_beyond_blind', 'outcome_relative_to_start','my_blind_anti_total', 
        'high_card', 'suited', 'pocket_pair', 'gap', 'hour','days_since_start', 'hand_frequency', 'low_card','card_rank',]]

    return result 

def train_test(X, y, rand_state = 151, test_size = .2):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state = rand_state)
    return X_train, X_test, y_train, y_test

# splits data for classification into training & holdout
def holdout_training_classification(): 
    df = pd.read_csv('/home/sam/Documents/DSI/capstone/poker/data/df_for_classification.csv')
    df = get_tournaments(df)
    df = put_in_money(df)
    df = df.dropna(subset = ['outcome_relative_to_start','buyin', 
                            'BB_in_stack', 'total_players', 'position',  
                            'low_card', 'high_card', 'suited', 'pocket_pair', 'card_rank' ])
    df = df[['buyin', 'BB_in_stack', 'total_players', 
             'position', 'low_card', 'high_card', 
             'suited', 'pocket_pair', 'card_rank', 
             'hour', 'days_since_start', 'hand_frequency', 'made_or_lost']]

    primary, holdout = train_test_split(df, test_size = .2)

    primary.to_csv('train_classification_tournaments.csv')
    holdout.to_csv('holdout_classification_tournaments.csv')
    



if __name__ == "__main__":
    # train = pd.read_csv('/home/sam/Documents/DSI/capstone/poker/data/train_classification_tournaments.csv')
    # hold = pd.read_csv('/home/sam/Documents/DSI/capstone/poker/data/holdout_classification_tournaments.csv')
    # print(train.info())
    # print(hold.info())

    df = pd.read_csv('new_df.csv')
    df = put_in_money(df)
    df = df.dropna(subset=['vpip_players_before', 'vpip_players_after'])
    print(df.info())