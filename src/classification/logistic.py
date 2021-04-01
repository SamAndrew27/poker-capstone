from sklearn.linear_model import LogisticRegression
import pandas as pd
from class_prep import read_in_return_Xy_no_time, grid_search


X, y = read_in_return_Xy_no_time()

lr = LogisticRegression(max_iter=5000)


if __name__ == "__main__":



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
    grid_search(X, y, lr, param_grid_elastic)

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
