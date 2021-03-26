from column_creation import fill_columns, load_df, X_y_regression
import pandas as pd 
import sqlite3
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import cross_val_score, train_test_split, GridSearchCV
import numpy as np 
from sklearn.preprocessing import MinMaxScaler

def knn_cv(X, y, p = 1, neighbors = 20):
    knn = KNeighborsRegressor(n_jobs = -1, p = p, n_neighbors=20)

    r2_score = cross_val_score(knn, X, y, n_jobs = -1, scoring= 'r2')
    mse = cross_val_score(knn, X, y, n_jobs = -1, scoring= 'neg_mean_squared_error')

    return f'R2: {np.mean(r2_score)} - MSE: {-np.mean(mse)}' 


# p_grid = {'n_neighbors': [3, 5, 10, 15, 20], 
#         'weights': ['uniform','distance'],
#         'p': [1, 2],
#         'n_jobs': [-1]} 


# knn_gscv = GridSearchCV(estimator= knn, param_grid=p_grid, n_jobs = -1, verbose=1, scoring='r2')

# knn_gscv.fit(X_scaled, y)

# print(knn_gscv.cv_results_)
# print(knn_gscv.best_estimator_)
# print(knn_gscv.best_score_)

if __name__ == "__main__":


    df = load_df()
    df = fill_columns(df)

    X, y = X_y_regression(df)

    scaler = MinMaxScaler()
    scaler.fit(X)
    X_scaled = scaler.transform(X)
    knn = KNeighborsRegressor()
    
    
    # leaf_size? algorithm? 


    print(knn_cv(X_scaled, y))

    # print(X_scaled)