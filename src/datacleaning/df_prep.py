import pandas as pd
from sklearn.model_selection import train_test_split

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
        'high_card', 'suited', 'pocket_pair', 'gap', 'hour','days_since_start', 'hand_frequency', 'low_card','card_rank',]]

    return result 

def train_test(X, y, rand_state = 151, test_size = .2):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state = rand_state)
    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    pass 