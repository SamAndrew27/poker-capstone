from sklearn.ensemble import GradientBoostingClassifier
import pandas as pd
from class_prep import read_in_return_Xy_no_time, grid_search, threshold_testing, confusion, confusion_ratios

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
    



    # param_grid6 = {'learning_rate': [.042],
    #             'n_estimators': [27,28,29,30,31, 32,33,34, 35,36,37,38,39, 40,41,42,43,44,45],
    #             'min_samples_leaf': [9],
    #             'min_samples_split': [2,3,4,5,6,7,8,9,10],
    #             'max_features': [2],
    #             'max_depth': [2],
    #             'subsample': [.18,.19,.2,.21, .22, .23, .24, .25, .26, .27,.28, .29,.3, .31, .32, .33, .34, .35, .36, .37, .38, .39, .4,.41,.42,.43,.44,.45]}




    thresholds = [.51,.52,.53,.54, .55, .56,.57,.58,.59,.6,.61,.62,.63,.64,.65]

    grad_boost = GradientBoostingClassifier(learning_rate=.042, max_depth=2, max_features=2, min_samples_leaf=9, min_samples_split=6, n_estimators=37, subsample=.3)
    thresh = .575
    3 # seems about right 
    # print(threshold_testing(X,y,grad_boost,thresholds))
    for num in [.54,.55,.56,.57,.58,.59,.6]:
        print(confusion_ratios(X,y,grad_boost,num, iterations = 1000))


    # {'thresh': 0.52, 'precision': 0.6196083205097493, 'npv': 0.6077334771762333, 'weighting': 0.8904534829359513}
    # {'thresh': 0.53, 'precision': 0.6297153306791561, 'npv': 0.5792698082394961, 'weighting': 0.8446283309957923}
    # {'thresh': 0.54, 'precision': 0.6361598586651769, 'npv': 0.5680656995598664, 'weighting': 0.7997007947639083}
    # {'thresh': 0.55, 'precision': 0.6496376811690955, 'npv': 0.5542131818975515, 'weighting': 0.7476671341748481}
    # {'thresh': 0.56, 'precision': 0.6577951750567421, 'npv': 0.5415472383645105, 'weighting': 0.6995792426367461}
    # {'thresh': 0.57, 'precision': 0.6649210058705944, 'npv': 0.5350690299077917, 'weighting': 0.6604675081813931}
    # {'thresh': 0.575, 'precision': 0.6671875058355616, 'npv': 0.5314234905436567, 'weighting': 0.6405002337540907}

    # 1000 iterations
    # {'thresh': 0.54, 'precision': 0.6386114146109487, 'npv': 0.564179072542559, 'weighting': 0.7978345021037868}
    # {'thresh': 0.55, 'precision': 0.6477260716220592, 'npv': 0.5514494176192678, 'weighting': 0.7494478728377746}
    # {'thresh': 0.56, 'precision': 0.6569571194287523, 'npv': 0.5435913085901394, 'weighting': 0.7045250116877045}
    # {'thresh': 0.57, 'precision': 0.6656705583002871, 'npv': 0.5366700101257501, 'weighting': 0.6610336605890603}
    # {'thresh': 0.58, 'precision': 0.6746464404603916, 'npv': 0.5255398076783029, 'weighting': 0.6131000467508181}
    # {'thresh': 0.59, 'precision': 0.6839690887370565, 'npv': 0.5126101174717648, 'weighting': 0.563386629266012}
    # {'thresh': 0.6, 'precision': 0.6930735568972298, 'npv': 0.5021561312730003, 'weighting': 0.5114763908368396}














    #    thresh        f1  accuracy precision    recall
    # 0    0.51  0.749196  0.616761  0.615211   0.95791
    # 1    0.51  0.748198  0.615941  0.615403  0.954884
    # 2    0.52  0.745043  0.621084  0.623412    0.9266
    # 3    0.53  0.736076  0.617694  0.626353  0.893762
    # 4    0.54  0.729452  0.623305  0.638972  0.850188
    # 5    0.55  0.721907  0.623889  0.646733  0.817353
    # 6    0.56  0.708403  0.623891  0.660178  0.765202
    # 7    0.57   0.69934  0.620267   0.66366  0.739531
    # 8    0.58  0.684026  0.617579  0.675556  0.693175
    # 9    0.59  0.667823  0.613254  0.686368   0.65036
    # 10    0.6  0.633145  0.597007  0.694904  0.582184
    # 11   0.61  0.607671   0.58766  0.704702  0.534336
    # 12   0.62  0.576838  0.575269  0.714697  0.485095
    # 13   0.63  0.520481   0.55283  0.722955  0.407434
    # 14   0.64  0.444438  0.527001  0.745745  0.317522
    # 15   0.65  0.385465  0.508765  0.762379  0.259194




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
    # GradientBoostingClassifier(learning_rate=0.042, max_depth=2, max_features=2,
    #                            min_samples_leaf=9, min_samples_split=9,
    #                            n_estimators=40, subsample=0.35)
