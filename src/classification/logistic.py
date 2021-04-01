from sklearn.linear_model import LogisticRegression
import pandas as pd
from class_prep import read_in_return_Xy_no_time, grid_search, threshold_testing, confusion


X, y = read_in_return_Xy_no_time()

lr = LogisticRegression(max_iter=5000)

lr_final = LogisticRegression(l1_ratio=.075, max_iter=5000, penalty='elasticnet', solver='saga')

if __name__ == "__main__":



    thresholds = [.45,.475, .505,.51, .515,.52,.525,.53, .535, .54, .55, .56,.57,.58,.59]

    # print(threshold_testing(X,y, lr_final, thresholds).sort_values('f1', ascending=False))


    print(confusion(X,y,lr_final,.545))




    param_grid_L1 = {'penalty': ['l1'],
                'class_weight': ['balanced', None],
                'solver': ['liblinear', 'saga']} #remove last 3 if this doesn't work

    param_grid_L2 = {'penalty': ['l2', 'none'],
                'class_weight': ['balanced', None],
                'solver': ['newton-cg', 'lbfgs', 'sag', 'saga']}#'liblinear'

    param_grid_elastic = {'penalty': ['elasticnet'],
                'class_weight': [None],
                'solver': ['saga'],
                'l1_ratio': [.075]}

    # grid_search(X, y, lr, param_grid_L1)
    # grid_search(X, y, lr, param_grid_L2)
    # grid_search(X, y, lr, param_grid_elastic)

    # L1
    # LogisticRegression(max_iter=10000, penalty='l1', solver='saga')
    # 0.7306848970377158

    # L2
    # LogisticRegression(max_iter=10000, solver='saga')
    # 0.7308508832657388

    # elastic
    # LogisticRegression(l1_ratio=0.08, max_iter=10000, penalty='elasticnet',
    #                    solver='saga')
    # 0.7308509193316699
    # LogisticRegression(l1_ratio=0.075, max_iter=5000, penalty='elasticnet',
    #                    solver='saga')
    # 0.7308509193316699


    #    thresh        f1  accuracy precision    recall
    # 0    0.45  0.743971  0.614188  0.616604  0.937875
    # 1   0.475   0.73889  0.615476  0.621852  0.910269
    # 2   0.505   0.72822  0.614543  0.629456  0.864157
    # 3    0.51  0.726051  0.614656  0.631333  0.854638
    # 4   0.515  0.722371   0.61302  0.632082  0.842859
    # 5    0.52  0.720962  0.614539  0.635539  0.833391
    # 6   0.525  0.719035   0.61489  0.637393  0.825268
    # 7    0.53  0.715559  0.613955  0.639299  0.812771
    # 8   0.535  0.712454  0.614073  0.642243  0.800476
    # 9    0.54  0.707901  0.611968   0.64333  0.786961
    # 10   0.55  0.702288   0.61267  0.649697  0.764327
    # 11   0.56  0.694331  0.613489   0.65834  0.734597
    # 12   0.57  0.680401  0.607411  0.662656  0.699623
    # 13   0.58  0.666585  0.603437  0.670054  0.663343
    # 14   0.59   0.65211  0.598994  0.677284  0.629115
