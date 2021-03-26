from column_creation import fill_columns, load_df, X_y_regression
import pandas as pd 
import sqlite3
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score, train_test_split, GridSearchCV
import numpy as np 

def rf_cv(X, y, md = 4, mf=2):
    rf = RandomForestRegressor(n_jobs= -1, max_features=mf, max_depth=md)
    r2_score = cross_val_score(rf, X, y, n_jobs= -1, scoring='r2')
    mse = cross_val_score(rf, X, y, n_jobs= -1, scoring='neg_mean_squared_error')

    return f'R2: {np.mean(r2_score)} - MSE: {-np.mean(mse)}' 


# not sure about the other parameters on this one, consider expanding 
# probably going to have to adjuste a lot of these if we add more features
rf = RandomForestRegressor()

p_grid = {'max_depth': [None, 4, 10], 
        'max_features': [2,3],
        'n_jobs': [-1]}

rf_gscv = GridSearchCV(estimator= rf, param_grid=p_grid, n_jobs = -1, verbose=1, scoring='r2')

rf_gscv.fit(X, y)

print(rf_gscv.cv_results_)
print(rf_gscv.best_estimator_)
print(rf_gscv.best_score_)

if __name__ == "__main__":
    df = load_df()
    df = fill_columns(df)
    X, y = X_y_regression(df)

    # print(rf_cv(X, y))

