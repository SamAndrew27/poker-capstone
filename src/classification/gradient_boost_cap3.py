from sklearn.ensemble import GradientBoostingClassifier
import pandas as pd
from data_prep import read_in_return_Xy_no_unused, read_in_return_Xy_scaled_no_unused
from grid_and_thresh_funcs import grid_search
from sklearn.model_selection import cross_val_score
import numpy as np
import pickle 

gb = GradientBoostingClassifier()

X, y = read_in_return_Xy_scaled_no_unused()

param_grid1 = {'learning_rate': [.05, .1, .2],
            'n_estimators': [50,100, 150,250,300],
            'min_samples_leaf': [1, 3, 5, 7, 10],
            'min_samples_split': [3,5,7,10],
            'max_features': [2,5,7],
            'max_depth': [2, 4, 6, 10],
            'subsample': [.2, .35, .5, .65, .8]}

# GradientBoostingClassifier(learning_rate=0.05, max_depth=2, max_features=3,
#                         min_samples_leaf=10, min_samples_split=3,
#                         n_estimators=50, subsample=0.5)
# 0.7601550244775049



param_grid2 = {'learning_rate': [.05, .1, .2],
            'n_estimators': [50,100,200],
            'min_samples_leaf': [2,6,10],
            'min_samples_split': [3,5,7,10],
            'max_features': [2,4,6,10],
            'max_depth': [2, 6, 10],
            'subsample': [.2, .3, .4, 5,.6, .7,.8,.9]}
# GradientBoostingClassifier(learning_rate=0.05, max_depth=2, max_features=2,
#                            min_samples_leaf=6, min_samples_split=3,
#                            n_estimators=50, subsample=0.2)
# 0.7592473166913645
# GradientBoostingClassifier(learning_rate=0.01, max_depth=6, max_features=3,
#                            min_samples_leaf=6, min_samples_split=4,
#                            n_estimators=70, subsample=0.6)
# 0.7615338553495826
# Fitting 5 folds for each of 120 candidates, totalling 600 fits
# GradientBoostingClassifier(learning_rate=0.015, max_depth=5, max_features=3,
#                            min_samples_leaf=6, min_samples_split=4,
#                            n_estimators=50, subsample=0.6)
# 0.7616200402100025


param_grid3 = {'learning_rate': [.01],
            'n_estimators': [90],
            'min_samples_leaf': [6],
            'min_samples_split': [4],
            'max_features': [3],
            'max_depth': [5],
            'subsample': [.2, .3, .4, .5, .6, .8]}
def feature_importance(model, X, y):
    cols = list(X.columns)

    model.fit(X,y)
    for idx, num in enumerate(model.feature_importances_):
        print(f'{cols[idx]}:{num}')

if __name__=="__main__":
    gb_final = GradientBoostingClassifier(learning_rate=.01, n_estimators=90, min_samples_leaf=6 , min_samples_split=4 ,max_features= 3,max_depth= 5,subsample= .6)
    # grid_search(X, y, gb, param_grid3)
    # subsample anywhere between .2-.8
    # seems to always prefer 2 & 3 for max depth max features

    # print(np.mean(cross_val_score(gb_final, X, y, scoring='f1')))
    # gb_final.fit(X,y)
    # pickle.dump(gb_final, open('gradient_boost_cap3.pickle', 'wb'))
    # feature_importance(gb_final, X, y)
    print(X.info())