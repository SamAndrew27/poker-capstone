import numpy as np 
import pandas as pd 
from data_prep import training_data_Xy, read_in_holdout_Xy
from sklearn.metrics import f1_score, confusion_matrix, accuracy_score, recall_score, precision_score, roc_auc_score, brier_score_loss



def test_values(true, pred):
    """input true/predicted to get results for various different metrics

    Args:
        true (array): array of true values
        pred (array): array of predicted values

    Returns:
        various metrics (floats or ints): precision, accuracy, recall, roc_auc, brier, f1, npv, tp, fp, tn, fn
    """    
    tn, fp, fn, tp = confusion_matrix(true, pred).ravel()
    accuracy = accuracy_score(true, pred)
    f1 = f1_score(true, pred)
    recall = recall_score(true, pred)
    precision = precision_score(true, pred)
    roc_auc = roc_auc_score(true,pred)
    brier = brier_score_loss(true,pred)
    npv =  tn/ (tn + fn)

    return precision, accuracy, recall, roc_auc, brier, f1, npv, tp, fp, tn, fn


def multiple_tests_random(iterations = 100 , probs=[0.405, 0.595]):
    """Runs multiple tests and finds the average metrics over those tests

    Args:
        iterations (int, optional): number of iterations to test. Defaults to 100.
        probs (list, optional): weighting of our random guessing, 2 valued list. First value is portion predicted negative, second value is portion predicted as positive. Defaults to [0.405, 0.595].

    Returns:
        DataFrame: DataFrame containing average scores of the relevant metrics 
    """    

    results = pd.DataFrame(columns=['precision', 'accuracy', 'recall', 'roc auc', 'brier', 'f1', 'npv', 'tp', 'fp', 'tn', 'fn' ], index=list(range(iterations)))
    _, y_hold = read_in_holdout_Xy()

    for idx in list(range(iterations)):


        predictions = pd.Series(data=np.random.choice(a=[0,1], size = len(y_hold), p=probs), index=y_hold.index)
        
        precision, accuracy, recall, roc_auc, brier, f1, npv, tp, fp, tn, fn = test_values(y_hold, predictions)
        results.iloc[idx] = [precision, accuracy, recall, roc_auc, brier, f1, npv, tp, fp, tn, fn]
    
    return results


if __name__=="__main__":
    
    # print(np.mean(multiple_tests_random(iterations=1000)))

    # WEIGHTED
    # precision      0.593202
    # accuracy       0.517849
    # recall         0.595250
    # roc auc        0.500140
    # brier          0.482151
    # f1             0.594183
    # npv            0.407087
    # tp           858.946000
    # fp           589.020000
    # tn           400.980000
    # fn           584.054000



    # unweighted
    # precision      0.593009
    # accuracy       0.499956
    # recall         0.500145
    # roc auc        0.499913
    # brier          0.500044
    # f1             0.542573
    # npv            0.406824
    # tp           721.709000
    # fp           495.315000
    # tn           494.685000
    # fn           721.291000

