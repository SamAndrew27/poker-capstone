import pandas as pd
from regression_prep import X_and_logged_y, grid_search, partial_plot, partial_plot_multiple, read_in_return_Xy_no_time, read_in_return_Xy
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import cross_val_score
import numpy as np 


X, y = X_and_logged_y()

X_no_time, y_no_time = read_in_return_Xy_no_time()

X_all, y_all = read_in_return_Xy()

gb = GradientBoostingRegressor(learning_rate = .1, n_estimators = 50, max_depth=2, max_features=3, min_samples_split=10)


# GradientBoostingRegressor(max_depth=2, max_features=3, min_samples_split=10)
# 0.012432983574568412


# GradientBoostingRegressor(max_depth=2, max_features=3, min_samples_split=11,
#                           n_estimators=50)
# 0.01255988780110382


# GradientBoostingRegressor(learning_rate=0.2, max_depth=2, max_features=3,
#                           min_samples_split=7, n_estimators=60)
# 0.01209312340700055


# GradientBoostingRegressor(max_depth=2, max_features=3, min_samples_split=10,
#                           n_estimators=50)
# 0.012943513390373317


# GradientBoostingRegressor(learning_rate=0.2, max_depth=2, max_features=3,
#                           min_samples_split=7, n_estimators=40)
# 0.01309920683077015
def cv(X, y, model):
    r2_score = cross_val_score(model, X, y, n_jobs = -1, scoring= 'r2')

    return f'R2: {np.mean(r2_score)}' 

if __name__ == "__main__":


    param_grid = {'learning_rate': [.05, .1,.15, .2, .25],
                'n_estimators': [40,45, 50, 55, 60,65, 70, 75, 90, 100,150,200,250,300,500,800,1000]}
                #'min_samples_leaf': [1,2, 3, 4]}

    #grid_search(X, y, gb, param_grid)
    # print(np.mean(X_all))
    #print(X_no_time['position'].value_counts())
    print(X_all.info())
    #artial_plot(X_all, y_all, gb, 10)
    partial_plot_multiple(X_no_time, y_no_time, gb, [4,7])
    # gb.fit(X_all, y_all)
    # print(gb.feature_importances_)