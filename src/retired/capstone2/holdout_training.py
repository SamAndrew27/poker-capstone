import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedShuffleSplit
from sklearn.preprocessing import StandardScaler
import numpy as np 

# splits tournaments from cash game (these functions unecessary now? our 'prior actions' function removes cash games ??? double check this)
def get_tournaments(df):
    """removes cash hands from df, leaving just tournaments

    Args:
        df (DataFrame): original DataFrame

    Returns:
        DataFrame: Dataframe of all tournament hands
    """    
    tourn_mask = df['cash_or_tourn'] == 'Holdem NL'        
    return df[tourn_mask]
    

def get_cash(df): # splits cash from tournament data
    """Removes tournaments from DataFrame

    Args:
        df (Dataframe): Original DataFrame

    Returns:
        DataFrame: all cash hands
    """    
    cash_mask = df['cash_or_tourn'] != 'Holdem NL'
    return df[cash_mask]


def put_in_money(df): # seperates tournaments where I put in $ versus tournaeents were I didn't
    """gets hands where I put in money besides what I blinded in 

    Args:
        df (DataFrame): Entire DataFrame

    Returns:
        DataFrame: DataFrame of hands where I put money in
    """    
    mask = df['money_beyond_blind'] == 1
    return df[mask]



# includes removing columns used in the creation of other columns
# just removing everything that couldn't potentially be used for model building
# removing both gametypes... OOPS (one is the one i created, useful for delineating cash from tournaments)
# BUT CONSIDER LOOKING AT THE ONE THEY CREATED! and naming the one I created something else 
# will create smaller columns as necessary 
def remove_unused_columns(df, drop = False):
    """removes unused columns - pretty sure this is something I used for regression, could probably retire

    Args:
        df (DataFrame): Entire DataFrame
        drop (bool, optional): If True drop first column. May be useful if data is coming directly from CSV. Defaults to False.

    Returns:
        DataFrame: only relevant columns included
    """    
    if drop:
        df = df.drop(df.columns[0], axis = 1)

    result = df[['buyin','won', 'bet','made_money','BB', 'BB_in_stack','starting_stack','total_players','table_max_players', 'position', 
        'flop_bet', 'turn_bet','river_bet', 'preflop_bet', 'net_outcome', 'all_in', 'money_beyond_blind', 'outcome_relative_to_start','my_blind_anti_total', 
        'high_card', 'suited', 'pocket_pair', 'gap', 'hour','days_since_start', 'hand_frequency', 'low_card','card_rank',]]

    return result 

def train_test(X, y, rand_state = 151, test_size = .2):
    """splits data into training and test

    Args:
        X (array): features
        y (array): target
        rand_state (int, optional): Random State. Defaults to 151.
        test_size (float, optional): Size of split (test size). Defaults to .2.

    Returns:
        4 arrays: training/test sets, features/targets
    """    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state = rand_state)
    return X_train, X_test, y_train, y_test


# splits data for classification into training & holdout
def holdout_training_classification(df): 
    """Splits data into training and classification. Uses functions above to remove certain rows. Drops data from relevant columns

    Args:
        df (DataFrame): DataFrame to split upon 
    """    
    df = get_tournaments(df)
    df = put_in_money(df)
    df = df.drop(df.columns[0], axis = 1)

    df = df.dropna(subset = ['BB_in_stack', # change this if you are using different columns (better done elsewhere?)
                             'position', 
                             'low_card', 
                             'high_card', 
                             'suited', 
                             'card_rank', 
                             'made_or_lost',
                             'limpers',
                             'raises&reraises',
                             'num_players_before',
                             'num_players_after'])

    primary, holdout = train_test_split(df, test_size = .2)

    primary.to_csv('../../data/train_classification_tournaments_4-25.csv')
    holdout.to_csv('../../data/holdout_classification_tournaments_4-25.csv')
    



if __name__ == "__main__":
    # train = pd.read_csv('/home/sam/Documents/DSI/capstone/poker/data/train_classification_tournaments.csv')
    # hold = pd.read_csv('/home/sam/Documents/DSI/capstone/poker/data/holdout_classification_tournaments.csv')
    # print(train.info())
    # print(hold.info())

    df = pd.read_csv('../../data/df_4-25.csv')
    holdout_training_classification(df)





    # 'amount_to_call',
    # 'average_table_vpip',
    # 'total_actions_witnessed',
    # 'vpip_relavant_players',

    # 'total_actions_witnessed_relevant_players',
    # 'weighted_relevant_vpip'