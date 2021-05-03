import pandas as pd
import sqlite3
from columns_from_hand_history import fill_HH_columns
from time_columns import fill_time_columns
from dependent_columns import fill_dependent_columns
from betting_columns_CALL_LAST import fill_betting_columns

def load_df(filepath="../../data/sql_data/dh_backup_20210425_060808/drivehud.db"):
    """loads sql DataBase and loads into pandas dataframe, performing a split on HandHistory for functions that use it to create columns

    Args:
        filepath (str, optional): Filepath to grab SQL data from. Defaults to "../../data/sql_data/dh_backup_20210425_060808/drivehud.db", which is what it is for me

    Returns:
        Pandas DataFrame: as contained in original backed up data (with HandHistory split)
    """    
    conn = sqlite3.connect(filepath)
    hand_history = pd.read_sql_query("select * from HandHistories;", conn)
    hand_history.HandHistory = hand_history.HandHistory.str.split('\r\n')

    df = hand_history.copy()

    return df 

def implement_column_creation(df, fill_BB_nans = True, prior_actions=True, time_columns=True):
    """creates all the columns using functions imported from other local files

    Args:
        df (DataFrame): DataFrame as stored in original backed up files
        fill_BB_nans (bool, optional): If True attempts to fill BB that have null values looking at other rows. Defaults to true
        prior_actions (bool, optional): If True will create 'prior_actions' column and all related columns. IN CURRENT FORM THIS DELETES ALL CASH HANDS. Defaults to True.
        time_columns (bool, optional): If True will create all time related columns. Defaults to True.

    Returns:
        DataFrame: final dataframe used for this project
    """    

    df = fill_HH_columns(df)    
    if time_columns:
        df = fill_time_columns(df)
    df = fill_dependent_columns(df, fill_BB_nans= fill_BB_nans, prior_actions=True)
    df = fill_betting_columns(df)

    return df 




if __name__ == "__main__":
    df = load_df()
    df = implement_column_creation(df)
    print(df.info())

    df.to_csv('../../data/df_4-25.csv')