from grid_and_thresh_funcs import grid_search
from data_prep import read_in_return_Xy_scaled_no_unused
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import f1_score
import numpy as np 
import pandas as pd

X, y = read_in_return_Xy_scaled_no_unused()

def model_eval(X, y, composite=True):
    """gets f1 score thru cross val of composite vs gradient boost

    Args:
        X (array): features
        y ([array]): target
        composite (bool, optional): composite vs gradient boost. if true composite. Defaults to True.

    Returns:
        float: average f1 score
    """    
    skf = StratifiedKFold(n_splits=5, shuffle=True)
    cvscores = []
    pre_predictions = pd.Series(index = X.index, dtype='float64') # Series to add the predictions from prelim models testing
    if composite:
        for train, test in skf.split(X, y):
            X_train = X.iloc[train]
            X_test = X.iloc[test]
            y_train = y.iloc[train]
            lr = LogisticRegression(l1_ratio=0.04, penalty='elasticnet', solver='saga')        
            lr.fit(X_train, y_train)
            pred = lr.predict_proba(X_test)[:,1]
            pre_predictions.iloc[test] = pred 

        X['prediction'] = pre_predictions 

    for train, test in skf.split(X, y):


        gb = GradientBoostingClassifier(learning_rate=.01, n_estimators=90, min_samples_leaf=6 , min_samples_split=4 ,max_features= 3,max_depth= 5,subsample= .6)
        gb.fit(X.iloc[train], y.iloc[train])
        pred = gb.predict(X.iloc[test])
        cvscores.append(f1_score(y.iloc[test], pred))
        # evaluate the model

    return np.mean(cvscores)

def compare_composite_v_gradient(X,y, iterations=1000):
    """compare composite vs gradient boost over some number of iterations, prints scores to terminal

    Args:
        X (array): features
        y (array): target
        iterations (int, optional): number of iterations Defaults to 1000.
    """    
    composite_results = []
    gb_results = []
    for num in range(iterations):
        gb_results.append(model_eval(X,y,composite=False))
        composite_results.append(model_eval(X,y,composite=True))
    print(f'Avg Composite:{np.mean(composite_results)}')
    print(f'Avg GB:{np.mean(gb_results)}')
    print(f'Min Composite:{min(composite_results)}')
    print(f'Min GB:{min(gb_results)}')
    print(f'Max Composite:{max(composite_results)}')
    print(f'Max GB:{max(gb_results)}')

if __name__=="__main__":
    compare_composite_v_gradient(X, y, iterations=1000)


    # Avg Composite:0.7620241618023208
    # Avg GB:0.7619449628765395
    # Min Composite:0.7586693770204608
    # Min GB:0.7585748351596532
    # Max Composite:0.7652504339876046
    # Max GB:0.7656764891890144
