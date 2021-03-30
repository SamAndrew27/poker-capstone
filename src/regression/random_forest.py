import pandas as pd
import numpy as np 
from sklearn.ensemble import RandomForestRegressor
from src.datacleaning.df_prep import train_test, remove_unused_columns, get_tournaments, put_in_money

df = pd.read_csv('/home/sam/Documents/DSI/capstone/poker/data/updated_DF.csv')

new_df = remove_unused_columns(df)