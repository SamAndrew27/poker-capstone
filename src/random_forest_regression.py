from column_creation import fill_columns, load_df, X_y_regression
import pandas as pd 
import sqlite3
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score, train_test_split
import numpy as np 

def rf_cv(X, y):
    rf = RandomForestRegressor(n_jobs= -1)
    r2_score = cross_val_score(rf, X, y, n_jobs= -1, scoring='r2')
    mse = cross_val_score(rf, X, y, n_jobs= -1, scoring='neg_mean_squared_error')

    return f'R2: {np.mean(r2_score)} - MSE: {-np.mean(mse)}' 


if __name__ == "__main__":
    df = load_df()
    df = fill_columns(df)
    X, y = X_y_regression(df)

    print(rf_cv(X, y))


