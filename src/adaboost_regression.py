from column_creation import fill_columns, load_df, X_y_regression
import pandas as pd 
import sqlite3
from sklearn.ensemble import AdaBoostRegressor
from sklearn.model_selection import cross_val_score, train_test_split, GridSearchCV
import numpy as np


df = load_df()
df = fill_columns(df)

X, y = X_y_regression(df)

def ada_cv(X, y):
    ada = AdaBoostRegressor()
    r2 = cross_val_score(ada, X, y, scoring='r2')
    mse = cross_val_score(ada, X, y, n_jobs= -1, scoring='neg_mean_squared_error')

    return f'R2: {np.mean(r2)} - MSE: {-np.mean(mse)}' 

if __name__ == "__main__":
    print(ada_cv(X, y))