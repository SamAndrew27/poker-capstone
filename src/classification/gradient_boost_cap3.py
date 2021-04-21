from sklearn.ensemble import GradientBoostingClassifier
import pandas as pd
from capstone3_data_prep import read_in_return_Xy_no_unused
from class_prep import grid_search


gb = GradientBoostingClassifier()

X, y = read_in_return_Xy_no_unused()

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
            'subsample': [.2, .4, .6, .8]}
GradientBoostingClassifier(learning_rate=0.05, max_depth=2, max_features=2,
                           min_samples_leaf=6, min_samples_split=3,
                           n_estimators=50, subsample=0.2)
0.7592473166913645

if __name__=="__main__":
    grid_search(X, y, gb, param_grid2)


    # GradientBoostingClassifier(learning_rate=0.05, max_depth=2, max_features=3,
    #                         min_samples_leaf=10, min_samples_split=3,
    #                         n_estimators=50, subsample=0.5)
    # 0.7601550244775049
