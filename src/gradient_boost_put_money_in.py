from regression_prep import first_regression_df
import pandas as pd
import numpy as np 
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV, cross_val_score

X, y = first_regression_df()





if __name__ == "__main__":
    gbr = GradientBoostingRegressor()

    p_grid = {'min_samples_split': [2,3,4,6], # consider looking at learning_rate, loss, 
                'max_features': [3,4,5,6,7],
                'max_depth': [2,3,4, 5,6],
                'min_samples_leaf': [1, 2,4,8]}
    
    gbr_gscv = GridSearchCV(estimator= gbr, param_grid=p_grid, n_jobs = -1, verbose=1, scoring='r2')

    gbr_gscv.fit(X, y)

    print(gbr_gscv.cv_results_)
    print(gbr_gscv.best_estimator_)
    print(gbr_gscv.best_score_)

    # GradientBoostingRegressor(max_depth=2, max_features=3, min_samples_leaf=8,
    #                       min_samples_split=4)
    # -0.10699239602796003
