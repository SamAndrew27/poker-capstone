from grid_and_thresh_funcs import grid_search
from data_prep import training_data_Xy
from sklearn.linear_model import LogisticRegression
import pandas as pd


lr = LogisticRegression(max_iter=10000)
X, y = training_data_Xy(scale=True)


param_grid_L1 = {'penalty': ['l1'],
            'class_weight': ['balanced', None],
            'solver': ['liblinear', 'saga']} #remove last 3 if this doesn't work

param_grid_L2 = {'penalty': ['l2', 'none'],
            'class_weight': ['balanced', None],
            'solver': ['newton-cg', 'lbfgs', 'sag', 'saga']}#'liblinear'

param_grid_elastic = {'penalty': ['elasticnet'],
            'class_weight': [None],
            'solver': ['saga'],
            'l1_ratio': [.035,.0375,.04,.0425,.045,.05,.055]}

if __name__== "__main__":
    # grid_search(X,y,lr, param_grid_L1)
    # LogisticRegression(penalty='l1', solver='saga')
    # 0.7456260473900602

    # grid_search(X,y,lr, param_grid_L2)
    # LogisticRegression(penalty='none', solver='newton-cg')
    # 0.7456245046815225
    grid_search(X,y,lr, param_grid_elastic)
    lr_final = LogisticRegression(l1_ratio=0.04, penalty='elasticnet', solver='saga')