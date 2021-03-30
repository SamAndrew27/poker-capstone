import pandas as pd
import numpy as np 
import inspect 
from regression_prep import get_tournaments, remove_unused_columns, train_test, put_in_money

df = pd.read_csv('/home/sam/Documents/DSI/capstone/poker/data/updated_DF.csv')
df = get_tournaments(df)
df = put_in_money(df)
X_train, X_test, y_train, y_test = train_test(df)











if __name__ == "__main__":
    pass