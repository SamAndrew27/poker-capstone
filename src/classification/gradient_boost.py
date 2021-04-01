from sklearn.ensemble import GradientBoostingClassifier
import pandas as pd
from class_prep import read_in_return_Xy_no_time, grid_search

X, y = read_in_return_Xy_no_time()


gb = GradientBoostingClassifier()

param_grid1 = {'learning_rate': [.05, .1, .2],
            'n_estimators': [50,100, 150],
            'min_samples_leaf': [1, 5, 10],
            'min_samples_split': [3,5,7],
            'max_features': [3,5,7],
            'max_depth': [2, 4, 6],
            'subsample': [.2, .5, .7]}

param_grid2 = {'learning_rate': [.05, .1],
            'n_estimators': [30,40,50,60,70],
            'min_samples_leaf': [8,10,12],
            'min_samples_split': [4,5,6],
            'max_features': [2,4,6],
            'max_depth': [2, 3],
            'subsample': [.15,.25,.35]}


param_grid3 = {'learning_rate': [ .025, .05, .075, .1],
            'n_estimators': [25,30,35],
            'min_samples_leaf': [8,9,10,11,12],
            'min_samples_split': [5,6,7],
            'max_features': [2,3],
            'max_depth': [2, 3],
            'subsample': [.2,.25,.3, .35]}

param_grid4 = {'learning_rate': [ .04, .05, .06],
            'n_estimators': [30,35,40,45,50],
            'min_samples_leaf': [8,9,10],
            'min_samples_split': [4,5,6,7],
            'max_features': [2,3],
            'max_depth': [2],
            'subsample': [.2,.25,.3, .35]}

param_grid5 = {'learning_rate': [.04, .0425, .045, .0475, .05],
            'n_estimators': [35,40,45],
            'min_samples_leaf': [9],
            'min_samples_split': [3,4,5,6,7,8],
            'max_features': [2],
            'max_depth': [2],
            'subsample': [.25,.3, .35, .4, .45,.5]}




if __name__ == "__main__":
    



    param_grid6 = {'learning_rate': [.042],
                'n_estimators': [27,28,29,30,31, 32,33,34, 35,36,37,38,39, 40,41,42,43,44,45],
                'min_samples_leaf': [9],
                'min_samples_split': [2,3,4,5,6,7,8,9,10],
                'max_features': [2],
                'max_depth': [2],
                'subsample': [.18,.19,.2,.21, .22, .23, .24, .25, .26, .27,.28, .29,.3, .31, .32, .33, .34, .35, .36, .37, .38, .39, .4,.41,.42,.43,.44,.45]}


    grid_search(X, y, gb, param_grid6)

    # pgrid1
    # GradientBoostingClassifier(learning_rate=0.05, max_depth=2, max_features=3,
    #                            min_samples_leaf=10, min_samples_split=5,
    #                            n_estimators=50, subsample=0.2)
    # 0.7416892636128869

    # pgrid2
    # GradientBoostingClassifier(learning_rate=0.05, max_depth=2, max_features=2,
    #                            min_samples_leaf=10, min_samples_split=6,
    #                            n_estimators=30, subsample=0.25)
    # 0.7514991765430205
    # GradientBoostingClassifier(learning_rate=0.05, max_depth=2, max_features=2,
    #                            min_samples_leaf=8, min_samples_split=6,
    #                            n_estimators=30, subsample=0.35)
    # 0.7520553537050483

    # param_grid3
    # GradientBoostingClassifier(learning_rate=0.05, max_depth=2, max_features=2,
    #                            min_samples_leaf=9, min_samples_split=5,
    #                            n_estimators=35, subsample=0.25)
    # 0.7521827329575677

    # param_grid4
    # GradientBoostingClassifier(learning_rate=0.04, max_depth=2, max_features=2,
    #                            min_samples_leaf=9, min_samples_split=4,
    #                            n_estimators=45, subsample=0.35)
    # 0.752163675592797

    # param_grid5
    # GradientBoostingClassifier(learning_rate=0.045, max_depth=2, max_features=2,
    #                            min_samples_leaf=9, min_samples_split=7,
    #                            n_estimators=35, subsample=0.3)
    # 0.7525856533230771
    # GradientBoostingClassifier(learning_rate=0.04, max_depth=2, max_features=2,
    #                            min_samples_leaf=10, min_samples_split=7,
    #                            n_estimators=35, subsample=0.35)
    # 0.752457342334925

    # param_grid6
    # GradientBoostingClassifier(learning_rate=0.0425, max_depth=2, max_features=2,
    #                            min_samples_leaf=9, min_samples_split=6,
    #                            n_estimators=35, subsample=0.3)
    # 0.7520989319762574
    # GradientBoostingClassifier(learning_rate=0.042, max_depth=2, max_features=2,
    #                            min_samples_leaf=9, min_samples_split=8,
    #                            n_estimators=38, subsample=0.28)
    # 0.7538606603370372
    # GradientBoostingClassifier(learning_rate=0.042, max_depth=2, max_features=2,
    #                            min_samples_leaf=9, min_samples_split=6,
    #                            n_estimators=31, subsample=0.21)
    # 0.7529492404217827
    # GradientBoostingClassifier(learning_rate=0.042, max_depth=2, max_features=2,
    #                            min_samples_leaf=9, min_samples_split=3,
    #                            n_estimators=39, subsample=0.4)
    # 0.7526787984263122
