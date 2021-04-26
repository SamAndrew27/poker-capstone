from sklearn.ensemble import GradientBoostingClassifier
import pandas as pd
from data_prep import read_in_return_Xy_no_unused, read_in_holdout_return_X_y
from sklearn.model_selection import cross_val_score
import numpy as np
from sklearn.metrics import f1_score, confusion_matrix, accuracy_score, recall_score, precision_score


def create_model_load_data():
    """loads data and creates model fitted w/ data

    Returns:
        model: fitted model
        X_hold: Holdout Data features
        y_hold: Holdout data targets
    """    
    model = GradientBoostingClassifier(learning_rate=.01, n_estimators=90, min_samples_leaf=6 , min_samples_split=4 ,max_features= 3,max_depth= 5,subsample= .6)
    X, y = read_in_return_Xy_no_unused()
    X_hold, y_hold = read_in_holdout_return_X_y()
    model.fit(X,y)
    return model, X_hold, y_hold

def predict_split_predictions(lower_thresh=.55, upper_thresh=.65):
    """predicts on holdout data, groups holdout data based on the prediction made on it by model according to predict_proba

    Args:
        lower_thresh (float, optional): lower threshold. Defaults to .55.
        upper_thresh (float, optional): upper threshold. Defaults to .65.

    Returns:
        three DataFrames: each with some portion of holdout data. include target (true), prediction, and predict_proba output
    """    
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
    """makes value 1 if it is above threshold, 0 if below

    Args:
        x (array of floats): predict_proba column
        lower (float): threshold or cutoff

    Returns:
        int: 1 if above or equal, 0 if below
    """    
    if x >= lower:
        return 1
    else:
        return 0

def split_columns(df):
    """slits dataframe into two arrays, prediction and truth

    Args:
        df (DataFrame): DataFrame (as created in predict_split_predictions)

    Returns:
        2 arrays: true values, predictions
    """    
    pred = df.loc[:, 'prediction']
    true = df.loc[:, 'true']

    return true, pred



def test_values(true, pred, middle=False):
    """tests true/predictions for various metrics

    Args:
        true (array): true values
        pred (array): predicted values
        middle (bool, optional): If middle = True, gets metrics for predictions as False as well as true. Defaults to False.

    Returns:
        DataFrame: contraining results
    """    
    iterations = 1
    if middle:
        iterations = 2
    results = pd.DataFrame(columns=['precision', 'accuracy', 'recall', 'f1', 'npv', 'tp', 'fp', 'tn', 'fn' ], index=list(range(iterations)))
    
    for num in range(iterations):
        if num ==1:
            pred = pred.apply(lambda x: 0)

        tn, fp, fn, tp = confusion_matrix(true, pred).ravel()
        accuracy = accuracy_score(true, pred)
        f1 = f1_score(true, pred)
        recall = recall_score(true, pred)

        if tp:
            precision = precision_score(true, pred)
        else:
            precision=0
        if tn:
            npv =  tn/ (tn + fn)
        else:
            npv = 0
        results.iloc[num] = [precision,accuracy, recall, f1, npv, tp, fp, tn, fn]

    return results

def run_multiple_test(lower_thresh=.51, upper_thresh=.65, iterations = 1000, save=True, split_middle=False):
    """gets metric results for 3 groupings, lower, middle, and upper. Upper is always predicted True, lower always false, middle can be True or False

    Args:
        lower_thresh (float, optional): Lowest cutoff threshold. Defaults to .51.
        upper_thresh (float, optional): Highest cutoff threshold. Defaults to .65.
        iterations (int, optional): number of times to test. Defaults to 1000.
        save (bool, optional): saves to CSV if true, otherwise returns DataFrames. Defaults to True.
        split_middle (bool, optional): if True predict middle as both True and False. Defaults to False.

    Returns:
        DataFrame: results, only returned if save = False
    """    


    lower_df = pd.DataFrame(columns=['precision', 'accuracy', 'recall', 'f1', 'npv', 'tp', 'fp', 'tn', 'fn' ], index=list(range(iterations)))
    middle_df = pd.DataFrame(columns=['precision', 'accuracy', 'recall', 'f1', 'npv', 'tp', 'fp', 'tn', 'fn' ], index=list(range(iterations * 2)))
    # middle_df_false = pd.DataFrame(columns=['precision', 'accuracy', 'recall', 'f1', 'npv', 'tp', 'fp', 'tn', 'fn' ], index=list(range(iterations)))
    top_df = pd.DataFrame(columns=['precision', 'accuracy', 'recall', 'f1', 'npv', 'tp', 'fp', 'tn', 'fn' ], index=list(range(iterations)))

    df_lst = [lower_df, middle_df, top_df]
    mid_idx = 0
    for idx in range(iterations):
        top, middle, lower = predict_split_predictions(lower_thresh, upper_thresh)
        results = [lower, middle, top]
        result_count = 0
        for df, result in zip(df_lst,results):
            if result_count == 1:
                middle = True
            else:
                middle = False
            true, pred = split_columns(result) 

            one_test = test_values(true,pred, middle=middle)
            if result_count == 1:
                df.iloc[mid_idx] = one_test.iloc[0]
                df.iloc[mid_idx + 1] = one_test.iloc[1]

                mid_idx += 2

            else:
                df.iloc[idx] = one_test.iloc[0]
            result_count +=1



    if split_middle: 
        middle_true_mask = middle_df.tn == 0
        middle_true = middle_df[middle_true_mask]
        middle_false_mask = middle_df.tp == 0
        middle_false = middle_df[middle_false_mask]

        if save:
            lower_df.to_csv('../../data/lower_50.csv')
            middle_false.to_csv('../../data/middle_false_50.csv')
            middle_true.to_csv('../../data/middle_true_50.csv')
            top_df.to_csv('../../data/top__50.csv')
        else:

            return lower_df, middle_true, middle_false, top_df
    
    else:
        lower_df.to_csv('../../data/lower_50.csv')
        middle_df.to_csv('../../data/middle_false_50.csv')
        top_df.to_csv('../../data/top__50.csv')
            
        if save:
            lower_df.to_csv('../../data/lower_50.csv')
            middle.to_csv('../../data/middle_false_50.csv')
            top_df.to_csv('../../data/top__50.csv')
        else:

            return lower_df, middle_df, top_df     

                

# must play = .655 & up 
# probably should play it = 0.595 - 0.655
# maybe not? 0.51 - 0.595
# Don't do it! 0.51 and down 

def run_test_single_thresh(thresh=.55, iterations = 10):
    """Same as function above but only with a single threshold considered, above predicted True, below predicted false

    Args:
        thresh (float, optional): cutoff for true vs false. Defaults to .55.
        iterations (int, optional): number of iterations to run. Defaults to 10.

    Returns:
        float: mean of all metrics 
    """    
    print(thresh)
    result = pd.DataFrame(columns=['precision', 'accuracy', 'recall', 'f1', 'npv', 'tp', 'fp', 'tn', 'fn' ], index=list(range(iterations)))
    for idx in range(iterations):
        model, X_hold, y_hold = create_model_load_data()
        pred = model.predict_proba(X_hold)[:,1]

        predictions = pd.DataFrame(data={'prediction_proba':pred})
        predictions['prediction'] = predictions['prediction_proba'].apply(lambda x: made__proba_predictions(x, thresh))

        one_test = test_values(y_hold, predictions['prediction'])
        result.iloc[idx] = one_test.iloc[0]



    return np.mean(result)

if __name__=="__main__":
    lower_df, middle_df_true,middle_df_false, top_df = run_multiple_test(lower_thresh=0.51, upper_thresh=0.595, save=False, iterations=50, split_middle=True)
    # lower_df, middle_true, middle_false, top_df = run_multiple_test(lower_thresh=0.51, upper_thresh=0.52, save=False, iterations=10, split_middle=True)

    # print(run_test_single_thresh(thresh=.595, iterations=50))

    # print(np.mean(top_df))
    print(np.mean(middle_df_true))
    print(np.mean(middle_df_false))

    # print(np.mean(lower_df))

    # top_thresh, middle_thresh, lower_thresh = predict_split_predictions(lower_thresh=.51, upper_thresh=.595)

    # top_thresh, middle_thresh, lower_thresh = predict_split_predictions()
    # _, X_hold, y_hold =     create_model_load_data()

    # true, pred = split_columns(middle_thresh)

    # print(test_values(true, pred, True))

    # print(top_thresh.tail(10))

    # print(len(top_thresh))
    # print(len(middle_thresh))
    # print(len(lower_thresh))
    # print(len(top_thresh) +len(middle_thresh) )
    # print(top_df.describe())
    # print(len(y_hold))
    # print('checking values')
    # print(top_thresh['prediction_proba'].min())
    # print(middle_thresh['prediction_proba'].max())
    # print(middle_thresh['prediction_proba'].min())
    # print(lower_thresh['prediction_proba'].max())

# should redo the ones that aren't specific df's and get scores for whole dataframe 

    # .655+ as positive
    # precision      0.775323
    # accuracy       0.556317
    # recall         0.354733
    # f1             0.486693
    # npv            0.474780
    # tp           511.880000
    # fp           148.360000
    # tn           841.640000
    # fn           931.120000

    # .595+ as positive
    # precision       0.714898
    # accuracy        0.661192
    # recall          0.713306
    # f1              0.714007
    # npv             0.583605
    # tp           1029.300000
    # fp            410.620000
    # tn            579.380000
    # fn            413.700000


    # .51+ as positive
    # precision       0.638821
    # accuracy        0.645623
    # recall          0.926112
    # f1              0.756091
    # npv             0.687542
    # tp           1336.380000
    # fp            755.580000
    # tn            234.420000
    # fn            106.620000


    # .655+ as postiive  ONLY THIS RANGE
    # precision      0.773433
    # accuracy       0.773433
    # recall         1.000000
    # f1             0.872235
    # npv            0.000000
    # tp           512.360000
    # fp           150.120000
    # tn             0.000000
    # fn             0.000000

    # .595-.655 as positive ONLY THIS RANGE
    # precision      0.332686
    # accuracy       0.500000
    # recall         0.500000
    # f1             0.399524
    # npv            0.167314
    # tp           258.070000
    # fp           129.920000
    # tn           129.920000
    # fn           258.070000

    # .51 - .595 as positive ONLY THIS RANGE
    # precision      0.469286
    # accuracy       0.469286
    # recall         1.000000
    # f1             0.638748
    # npv            0.000000
    # tp           309.020000
    # fp           348.940000
    # tn             0.000000
    # fn             0.000000



    # .51 - .595 as negative ONLY THIS RANGE
    # precision      0.000000
    # accuracy       0.530714
    # recall         0.000000
    # f1             0.000000
    # npv            0.530714
    # tp             0.000000
    # fp             0.000000
    # tn           348.940000
    # fn           309.020000







# SCORES BEFORE ADDITIONAL rows!!!
#######################################################################################################
    # range .595 to 0.655 alone predicted as positive
    # precision      0.669145
    # accuracy       0.669145
    # recall         1.000000
    # f1             0.801763
    # npv            0.000000
    # tp           425.700000
    # fp           210.500000
    # tn             0.000000
    # fn             0.000000

    # range .595 to 0.655 alone predicted as negative
    # precision      0.000000
    # accuracy       0.330865
    # recall         0.000000
    # f1             0.000000
    # npv            0.330865
    # tp             0.000000
    # fp             0.000000
    # tn           211.200000
    # fn           427.400000



    # range .51 to .595 alone predicted as positive
    # precision      0.524221
    # accuracy       0.524221
    # recall         1.000000
    # f1             0.687825
    # npv            0.000000
    # tp           337.200000
    # fp           305.700000
    # tn             0.000000
    # fn             0.000000

    # range .51 to .595 alone predicted as negative
    # precision      0.000000
    # accuracy       0.475779
    # recall         0.000000
    # f1             0.000000
    # npv            0.475779
    # tp             0.000000
    # fp             0.000000
    # tn           305.700000
    # fn           337.200000


    # .655+ as positive
    # precision      0.766035
    # accuracy       0.543600
    # recall         0.340031
    # f1             0.470943
    # npv            0.463340
    # tp           434.560000
    # fp           132.800000
    # tn           728.200000
    # fn           843.440000
    # dtype: float64

    # .595 + as positive
    # precision      0.714066
    # accuracy       0.642777
    # recall         0.670704
    # f1             0.691627
    # npv            0.551796
    # tp           857.160000
    # fp           343.260000
    # tn           517.740000
    # fn           420.840000






    # .51+ as positive
    # precision       0.647487
    # accuracy        0.657943
    # recall          0.938388
    # f1              0.766256
    # npv             0.725505
    # tp           1199.260000
    # fp            652.920000
    # tn            208.080000
    # fn             78.740000











































    # range .595 and up predicted as positive
    # precision      0.713519
    # accuracy       0.713519
    # recall         1.000000
    # f1             0.832808
    # npv            0.000000
    # tp           861.700000
    # fp           346.000000
    # tn             0.000000
    # fn             0.000000
    # dtype: float64





# # Counting 0.51 as all positive 
# precision       0.647646
# accuracy        0.647646
# recall          1.000000
# f1              0.786146
# npv             0.000000
# tp           1199.500000
# fp            652.600000
# tn              0.000000
# fn              0.000000


    # for range over 0.655
    # precision      0.767814
    # accuracy       0.767814
    # recall         1.000000
    # f1             0.868642
    # npv            0.000000
    # tp           432.000000
    # fp           130.700000
    # tn             0.000000
    # fn             0.000000