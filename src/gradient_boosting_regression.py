from column_creation import fill_columns, load_df, X_y_regression
import pandas as pd 
import sqlite3
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import cross_val_score, train_test_split, GridSearchCV
import numpy as np

df = load_df()
df = fill_columns(df)

X, y = X_y_regression(df)

def gbr_cv(X, y):
    gbr = GradientBoostingRegressor()
    r2_score = cross_val_score(gbr, X, y, n_jobs = -1, scoring= 'r2')
    mse = cross_val_score(gbr, X, y, n_jobs = -1, scoring= 'neg_mean_squared_error')

    return f'R2: {np.mean(r2_score)} - MSE: {-np.mean(mse)}' 




if __name__ == "__main__":


    gbr = GradientBoostingRegressor()
    
    X_train, X_test, y_train, y_test = train_test_split(X, y)

    p_grid = {'learning_rate': [.05, .1, .2],
              'max_features': [2,3],
              'max_depth': [2,3,4],
              'subsample': [.25, .5, .75, 1]}
    
    gbr_gscv = GridSearchCV(estimator= gbr, param_grid=p_grid, n_jobs = -1, verbose=2, scoring='r2')

    gbr_gscv.fit(X, y)

    print(gbr_gscv.cv_results_)
    print(gbr_gscv.best_estimator_)
    print(gbr_gscv.best_score_)

    

'''
GradientBoostingRegressor(learning_rate=0.05, max_depth=2, max_features=2,
                          subsample=0.75)
-0.04141028766302175

'''
    
