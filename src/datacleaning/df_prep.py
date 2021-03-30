import pandas as pd


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
def remove_unused_columns(df):
    result = df.drop(df.columns[0], axis = 1)
    result = result[['buyin','my_blind_anti_total', 
       'starting_stack',  'won', 'bet', 'made_money',
       'total_players', 'card_rank', 'position', 'BB', 'BB_in_stack',
       'net_outcome', 'all_in', 'money_beyond_blind', 'hour',
       'days_since_start', 'hand_frequency', 'flop_bet', 'turn_bet',
       'river_bet', 'preflop_bet', 'high_card', 'suited', 'pocket_pair', 'gap',
       'low_card', 'table_max_players', 'outcome_relative_to_start']]


if __name__ == "__main__":
    pass 