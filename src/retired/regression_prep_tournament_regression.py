import pandas as pd
from sklearn.model_selection import train_test_split, ShuffleSplit

# splits cash games from tournaments 
def get_tournaments(df):
    tourn_mask = df['cash_or_tourn'] == 'Holdem NL'        
    return df[tourn_mask]
    

def get_cash(df):
    cash_mask = df['cash_or_tourn'] != 'Holdem NL'
    return df[cash_mask]


def put_in_money(df):
    mask = df['money_beyond_blind'] == 1
    return df[mask]

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
         'suited', 'pocket_pair', 'gap', 'hour','days_since_start', 'hand_frequency', 'low_card','high_card','card_rank']]

    return result 

def train_test(X, y, rand_state = 151, test_size = .2):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state = rand_state)
    return X_train, X_test, y_train, y_test

def split_for_regression():
    df = pd.read_csv('/home/sam/Documents/DSI/capstone/poker/data/updated_DF.csv')

    df = get_tournaments(df)
    df = put_in_money(df)
    remove_unused_columns(df)
    X = df[['buyin', 'total_players', 'position', 
            'suited',  'low_card','high_card','card_rank','hour',
            'days_since_start', 'hand_frequency', 'outcome_relative_to_start']]
    X = X.dropna()
    y = X['outcome_relative_to_start']
    del X['outcome_relative_to_start']

    X_train, X_holdout, y_train, y_holdout = train_test(X, y)

    return X_train, y_train

def split_for_regression_no_BB():
    df = pd.read_csv('/home/sam/Documents/DSI/capstone/poker/data/updated_DF.csv')

    df = get_tournaments(df)
    df = put_in_money(df)
    remove_unused_columns(df)
    X = df[['buyin', 'total_players', 'position', 
            'suited',  'low_card','high_card','card_rank','hour',
            'days_since_start', 'hand_frequency', 'outcome_relative_to_start']]
    X = X.dropna()
    y = X['outcome_relative_to_start']
    del X['outcome_relative_to_start']

    X_train, X_holdout, y_train, y_holdout = train_test(X, y)

    return X_train, y_train


def split_for_regression_no_time():
    df = pd.read_csv('/home/sam/Documents/DSI/capstone/poker/data/updated_DF.csv')

    df = get_tournaments(df)
    df = put_in_money(df)
    remove_unused_columns(df)
    X = df[['buyin', 'BB_in_stack', 'total_players', 'position', 
            'suited',  'low_card','high_card',
            'card_rank','outcome_relative_to_start']]
    X = X.dropna()
    y = X['outcome_relative_to_start']
    del X['outcome_relative_to_start']

    X_train, X_holdout, y_train, y_holdout = train_test(X, y)

    return X_train, y_train


def holdout_and_primary_tournaments():
    df = pd.read_csv('/home/sam/Documents/DSI/capstone/poker/data/updated_DF.csv')
    df = get_tournaments(df)
    df = put_in_money(df)
    df = df.dropna(subset = ['position', 'BB_in_stack'])
    
    primary, holdout = train_test_split(df, test_size = .2)

    primary.to_csv('train_tournaments.csv')
    holdout.to_csv('holdout_tournaments.csv')
    
def read_in_holdout_and_split():
    df = pd.read_csv('/home/sam/Documents/DSI/capstone/poker/data/train.csv')



if __name__ == "__main__":
    # df = pd.read_csv('/home/sam/Documents/DSI/capstone/poker/data/updated_DF.csv')
    # df = get_tournaments(df)
    # df = put_in_money(df)
    holdout_and_primary_tournaments()