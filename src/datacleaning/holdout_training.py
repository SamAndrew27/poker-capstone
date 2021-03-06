import numpy as np 
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedShuffleSplit
from sklearn.preprocessing import StandardScaler

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




def holdout_training_classification(df, filename='default'): 
    """Splits data into training and classification. Uses functions above to remove certain rows. Drops data from relevant columns
    Saves holdout/training to 2 csv files

    Args:
        df (DataFrame): DataFrame to split upon 
        filename (str, optional): filename for holdout/training, comes after 'training' or 'holdout' in name. Defaults to 'default'.
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

    primary.to_csv(f'../../data/train{filename}.csv')
    holdout.to_csv(f'../../data/holdout{filename}.csv')
    



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