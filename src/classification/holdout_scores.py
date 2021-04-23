from sklearn.ensemble import GradientBoostingClassifier
import pandas as pd
from capstone3_data_prep import read_in_return_Xy_no_unused, read_in_holdout_return_X_y
from class_prep import grid_search
from sklearn.model_selection import cross_val_score
import numpy as np
from sklearn.metrics import f1_score, confusion_matrix, accuracy_score, recall_score, precision_score


def create_model_load_data():
    model = GradientBoostingClassifier(learning_rate=.01, n_estimators=90, min_samples_leaf=6 , min_samples_split=4 ,max_features= 3,max_depth= 5,subsample= .6)
    X, y = read_in_return_Xy_no_unused()
    X_hold, y_hold = read_in_holdout_return_X_y()
    model.fit(X,y)
    return model, X_hold, y_hold

def predict_split_predictions(lower_thresh=.55, upper_thresh=.65):
    model, X_hold, y_hold = create_model_load_data()
    y_pred = model.predict_proba(X_hold)
    results = pd.DataFrame(data={'true':y_hold, 'prediction_proba':y_pred[:,1]})
    results['prediction'] = results['prediction_proba'].apply(lambda x: made__proba_predictions(x, lower_thresh))
    mask_highest = results['prediction_proba'] >= upper_thresh
    top_thresh = results[mask_highest]

    mask_middle = (results['prediction_proba'] < upper_thresh) & (results['prediction_proba'] > lower_thresh)
    middle_thresh = results[mask_middle] 

    mask_bottom = results['prediction_proba'] <= lower_thresh
    lower_thresh = results[mask_bottom] 

    return top_thresh, middle_thresh, lower_thresh



def made__proba_predictions(x, lower):
    if x >= lower:
        return 1
    else:
        return 0

def split_columns(df):
    pred = df.loc[:, 'prediction']
    true = df.loc[:, 'true']

    return true, pred



def test_values(true, pred, middle=False):
    iterations = 1
    if middle:
        iterations = 2
    results = pd.DataFrame(columns=['precision', 'accuracy', 'recall', 'f1', 'npv', 'tp', 'fp', 'tn', 'fn' ], index=list(range(iterations)))
    
    for num in range(iterations):
        if num ==1:
            pred = pred.apply(lambda x: 0)

        tn, fp, fn, tp = confusion_matrix(true, pred).ravel()
        precision = precision_score(true, pred)
        accuracy = accuracy_score(true, pred)
        f1 = f1_score(true, pred)
        recall = recall_score(true, pred)
        npv =  tn/ (tn + fn)
        results.iloc[num] = [precision,accuracy, recall, f1, npv, tp, fp, tn, fn]

    return results

def run_multiple_test(lower_thresh=.55, upper_thresh=.65, iterations = 1000):


    lower_df = pd.DataFrame(columns=['precision', 'accuracy', 'recall', 'f1', 'npv', 'tp', 'fp', 'tn', 'fn' ], index=list(range(iterations)))
    middle_df = pd.DataFrame(columns=['precision', 'accuracy', 'recall', 'f1', 'npv', 'tp', 'fp', 'tn', 'fn' ], index=list(range(iterations * 2)))
    # middle_df_false = pd.DataFrame(columns=['precision', 'accuracy', 'recall', 'f1', 'npv', 'tp', 'fp', 'tn', 'fn' ], index=list(range(iterations)))
    top_df = pd.DataFrame(columns=['precision', 'accuracy', 'recall', 'f1', 'npv', 'tp', 'fp', 'tn', 'fn' ], index=list(range(iterations)))

    df_lst = [lower_df, middle_df, top_df]
    
    for idx in range(iterations):
        top, middle, lower = predict_split_predictions()
        results = [lower, middle, top]
        count = 0
        for df, result in zip(df_lst,results):
            if count == 1:
                middle = True
            else:
                middle = False
            true, pred = split_columns(result) 
            one_test = test_values(true,pred, middle=middle)
            df.iloc[idx] = one_test.
            count += 1
    
    return lower_df

            
            

                
            




if __name__=="__main__":
    run_multiple_test(iterations=10)

    # top_thresh, middle_thresh, lower_thresh = predict_split_predictions()
    # _, X_hold, y_hold =     create_model_load_data()

    # true, pred = split_columns(middle_thresh)

    # print(test_values(true, pred, True))

    # print(top_thresh.tail(10))

    # print(len(top_thresh))
    # print(len(middle_thresh))
    # print(len(lower_thresh))
    # print(len(y_hold))
    # print('checking values')
    # print(top_thresh['prediction_proba'].min())
    # print(middle_thresh['prediction_proba'].max())
    # print(middle_thresh['prediction_proba'].min())
    # print(lower_thresh['prediction_proba'].max())




