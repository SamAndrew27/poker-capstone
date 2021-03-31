import pandas as pd
from regression_prep import X_and_logged_y, grid_search, partial_plot, partial_plot_multiple, read_in_return_Xy_no_time, read_in_return_Xy, scaled_and_logged_X_y
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import cross_val_score
import numpy as np 

X_scaled, y_logged = scaled_and_logged_X_y()
X, y = X_and_logged_y()

X_no_time, y_no_time = read_in_return_Xy_no_time()

X_all, y_all = read_in_return_Xy()

gb = GradientBoostingRegressor(learning_rate=.15, n_estimators = 50, max_depth=2, max_features=3, min_samples_split=10)



'''
not totally sure why I put this in here, probably better to keep
it in a seperate file? if at all, note sure why I was using this
'''
def cv(X, y, model):
    r2_score = cross_val_score(model, X, y, n_jobs = -1, scoring= 'r2')

    return f'R2: {np.mean(r2_score)}' 

if __name__ == "__main__":


    param_grid = {'learning_rate': [.05, .1, .15],
                'n_estimators': [60,70,80,90,100],
                'min_samples_leaf': [1,2,3],
                'min_samples_split': [3,4,5,6,7],
                'max_features': [4,5,6,7],
                'max_depth': [2, 3,4],
                'subsample': [1.,.15,.25, .35, .5]}

    grid_search(X_scaled, y_logged, gb, param_grid)
    # print(np.mean(X_all))
    #print(X_no_time['position'].value_counts())
    # print(X_all.info())
    #partial_plot(X_no_time, y_no_time, gb, 3)
    # partial_plot_multiple(X_no_time, y_no_time, gb, [4,7])
    # gb.fit(X_all, y_all)
    # print(gb.feature_importances_)


    #print(cv(X_scaled, y_logged, gb))



# RESULT

# GradientBoostingRegressor(learning_rate=0.05, max_depth=2, max_features=6,
#                           min_samples_split=7, n_estimators=80, subsample=0.5)
# 0.014081467921514813


# GradientBoostingRegressor(max_depth=2, max_features=6, min_samples_split=5,
#                           n_estimators=80, subsample=0.25)
# 0.014267438283174338



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

# GradientBoostingRegressor(learning_rate=0.2, max_depth=2, max_features=3,
#                           min_samples_split=10, n_estimators=50)
# 0.012552655390747458

# GradientBoostingRegressor(learning_rate=0.16, max_depth=2, max_features=3,
#                           min_samples_split=10, n_estimators=t)
# 0.013205381932133897


