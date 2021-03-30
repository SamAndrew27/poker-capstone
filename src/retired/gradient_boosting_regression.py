from column_creation import fill_columns, load_df, X_y_regression
import pandas as pd 
import sqlite3
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import cross_val_score, train_test_split, GridSearchCV
import numpy as np

df = load_df()
df = fill_columns(df)

X, y = X_y_regression(df)






# Grid Search, consider expanding upon this (more metrics, more values for metrics)

p_grid = {'min_samples_split': [2,3,4,6], # consider looking at learning_rate, loss, 
            'max_features': [3,4,5,6,7],
            'max_depth': [2,3,4, 5,6],
            'min_samples_leaf': [1, 2,4,8]}

# gbr_gscv = GridSearchCV(estimator= gbr, param_grid=p_grid, n_jobs = -1, verbose=1, scoring='r2')

# gbr_gscv.fit(X, y)

# print(gbr_gscv.cv_results_)
# print(gbr_gscv.best_estimator_)
# print(gbr_gscv.best_score_)

if __name__ == "__main__":


    gbr = GradientBoostingRegressor()
    
    X_train, X_test, y_train, y_test = train_test_split(X, y)



    print(gbr_cv(X, y))

    '''
    GradientBoostingRegressor(learning_rate=0.05, max_depth=2, max_features=2,
                            subsample=0.75)
    -0.04141028766302175

    '''
        
