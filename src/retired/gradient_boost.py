import pandas as pd
import numpy as np 
import inspect 
from regression_prep_tournament_regression import split_for_regression, split_for_regression_no_BB, split_for_regression_no_time
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.inspection import plot_partial_dependence




X_train, y_train = split_for_regression()
X_no_BB, y_no_BB = split_for_regression_no_BB()
X_no_time, y_no_time = split_for_regression_no_time()

def grid_search_gbr(X, y, param_grid = None):
    gbr = GradientBoostingRegressor()
    if param_grid == None:
        param_grid = {'min_samples_split': [2,3,4,6], # consider looking at learning_rate, loss, 
                    'max_features': [3,4,5,6,7],
                    'max_depth': [2,3,4, 5,6],
                    'min_samples_leaf': [1, 2,4,8]}
    
    gbr_gscv = GridSearchCV(estimator= gbr, param_grid=param_grid, n_jobs = -1, verbose=1, scoring='r2')

    gbr_gscv.fit(X, y)

    print(gbr_gscv.best_estimator_)
    print(gbr_gscv.best_score_)  

    # USING ALL AVAILABLE COLUMNS 
    # GradientBoostingRegressor(max_depth=2, max_features=3, min_samples_leaf=4,
    #                       min_samples_split=6)
    # 0.01230070583637075

    # NO BB_in_stack
    # GradientBoostingRegressor(max_depth=2, max_features=3, min_samples_leaf=4,
    #                       min_samples_split=4)
    # 0.007880577200452366

    # NO TIME
    # GradientBoostingRegressor(max_depth=2, max_features=3, min_samples_leaf=8)
    # 0.014154643870696116


def gbr_cv(X, y, lr = .05, n_est = 100, mf = 2, md = 2, msl = 8, mss = 4):
    gbr = GradientBoostingRegressor(learning_rate= lr, n_estimators=n_est, max_depth= md, max_features= mf, min_samples_leaf=msl, min_samples_split=mss)
    r2_score = cross_val_score(gbr, X, y, n_jobs = -1, scoring= 'r2')
    mse = cross_val_score(gbr, X, y, n_jobs = -1, scoring= 'neg_mean_squared_error')

    return f'R2: {np.mean(r2_score)} - MSE: {-np.mean(mse)}' 


if __name__ == "__main__":
    # GETTING FEATURE IMPORTANCES WITH ALL COLUMNS
    # print(gbr_cv(X_train, y_train, mf = 3, msl = 4, mss = 6))
    gbr = GradientBoostingRegressor()
    gbr.fit(X_train, y_train)
    print(X_train.columns)
    print(gbr.feature_importances_)
    print(np.mean(y_train))
    #grid_search_gbr(X_no_BB, y_no_BB)
    #grid_search_gbr(X_no_time, y_no_time)
