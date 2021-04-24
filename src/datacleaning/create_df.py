import pandas as pd
import sqlite3
from columns_from_hand_history import fill_HH_columns
from time_columns import fill_time_columns
from dependent_columns import fill_dependent_columns
from betting_columns_CALL_LAST import fill_betting_columns

def load_df():
    conn = sqlite3.connect("/home/sam/Documents/DSI/capstone/poker/data/sql_data/dh_backup_20210330_081745/drivehud.db")
    hand_history = pd.read_sql_query("select * from HandHistories;", conn)
    hand_history.HandHistory = hand_history.HandHistory.str.split('\r\n')

    df = hand_history.copy()

    return df 

def implement_column_creation(df, fill_BB_nans = True):
    df = fill_HH_columns(df)    
    df = fill_time_columns(df)
    df = fill_dependent_columns(df, fill_BB_nans= fill_BB_nans)
    df = fill_betting_columns(df)

    return df 




if __name__ == "__main__":
    df = load_df()
    df = implement_column_creation(df)
    print(df.info())

    df.to_csv('df_4-24.csv')