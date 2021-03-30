import pandas as pd  
import numpy as np 
from column_creation import load_df, fill_columns, split_cash

def first_regression_df():
    read_in = pd.read_csv('/home/sam/Documents/DSI/capstone/poker/data/full_dataframe.csv')

    tourn, ____ = split_cash(read_in)

    mask = tourn['money_beyond_blind'] ==1
    put_in_money = tourn[mask]

    put_in_money.dropna(inplace=True)
    df = put_in_money[['buyin','my_blind_anti_total','position', 'BB_in_stack', 'net_outcome','high_card', 'suited', 'pocket_pair', 'low_card', 'table_max_players']]

    y = df['net_outcome']
    del df['net_outcome']
    X = df.copy()

    return X, y


def second_regression_df():

    read_in = pd.read_csv('/home/sam/Documents/DSI/capstone/poker/data/full_dataframe.csv')

    tourn, ____ = split_cash(read_in)

    mask = tourn['money_beyond_blind'] ==1
    put_in_money = tourn[mask]

    put_in_money.dropna(inplace=True)
    df = put_in_money[['buyin','starting_stack','position', 'BB_in_stack', 'net_outcome','high_card', 'suited', 'pocket_pair', 'low_card', 'table_max_players']]

    y = df['net_outcome']
    del df['net_outcome']
    X = df.copy()

    return X, y


def third_regression_df():

    read_in = pd.read_csv('/home/sam/Documents/DSI/capstone/poker/data/full_dataframe.csv')

    tourn, ____ = split_cash(read_in)

    mask = tourn['money_beyond_blind'] ==1
    put_in_money = tourn[mask]

    put_in_money.dropna(inplace=True)
    df = put_in_money[['buyin','position', 'BB_in_stack', 'outcome_relative_to_start','high_card', 'suited', 'pocket_pair', 'low_card', 'table_max_players']]

    y = df['outcome_relative_to_start']
    del df['outcome_relative_to_start']
    X = df.copy()

    return X, y

if __name__ == "__main__":
    old = pd.read_csv('/home/sam/Documents/DSI/capstone/poker/data/full_dataframe.csv')
    new = pd.read_csv('/home/sam/Documents/DSI/capstone/poker/data/all_my_data.csv')

    print(old.info())
    print(new.info())