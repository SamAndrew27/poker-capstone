from class_prep import read_in_return_Xy_no_time, confusion_ratios
from sklearn.ensemble import GradientBoostingClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, accuracy_score, recall_score, precision_score
import pandas as pd 
import numpy as np 
from sklearn.model_selection import KFold

def composite_model(X, y, primary_model, preliminary_model1, preliminary_model2, num_folds=5, thresh=.5): # primary model does the final regression, preliminary produces prediction for primary to factor in

    kf = KFold(n_splits=num_folds, shuffle=True)
    error = np.empty(num_folds)
    index = 0
    pre_predictions1 = pd.Series(index = X.index, dtype='float64') # Series to add the predictions from prelim models testing
    pre_predictions2 = pd.Series(index = X.index, dtype='float64')

    for train, test in kf.split(X):
        X_train = X.iloc[train]
        X_test = X.iloc[test]
        y_train = y.iloc[train]


        preliminary_model1.fit(X_train, y_train) # running through both models and adding to respective series
        prediction1 = preliminary_model1.predict_proba(X_test) 
        prediction1 = prediction1[:,1]
        pre_predictions1.iloc[test] = prediction1


        preliminary_model2.fit(X_train, y_train) 
        predictions2 = preliminary_model2.predict_proba(X_test) 
        predictions2 = predictions2[:,1]
        pre_predictions2.iloc[test] = predictions2



    X['prediction1'] = pre_predictions1 # add series to dataframe as columns
    X['prediction2'] = pre_predictions2


    for train, test in kf.split(X):
        X_train = X.iloc[train]
        X_test = X.iloc[test]
        y_train = y.iloc[train]
        y_test = y.iloc[test]        

        primary_model.fit(X_train, y_train)
        final_prediction = primary_model.predict(X_test) # get prediction

        error[index] = f1_score(y_test,final_prediction) 
        index += 1


    return np.mean(error)


def thresh_testing_composite(X, y, primary_model, preliminary_model1, preliminary_model2, thresholds = [.5], num_folds=5):
    kf = KFold(n_splits=num_folds, shuffle=True)
    results = pd.DataFrame(columns=['thresh', 'f1', 'accuracy', 'precision','recall'],index=list(range(0, len(thresholds)))) # stores the results of all theshold tests


    pre_predictions1 = pd.Series(index = X.index, dtype='float64') # Series to add the predictions from prelim models testing
    pre_predictions2 = pd.Series(index = X.index, dtype='float64')

    for train, test in kf.split(X):
        X_train = X.iloc[train]
        X_test = X.iloc[test]
        y_train = y.iloc[train]


        preliminary_model1.fit(X_train, y_train) # running through both models and adding to respective series
        prediction1 = preliminary_model1.predict_proba(X_test) 
        prediction1 = prediction1[:,1]
        pre_predictions1.iloc[test] = prediction1


        preliminary_model2.fit(X_train, y_train) 
        predictions2 = preliminary_model2.predict_proba(X_test) 
        predictions2 = predictions2[:,1]
        pre_predictions2.iloc[test] = predictions2



    X['prediction1'] = pre_predictions1 # add series to dataframe as columns
    X['prediction2'] = pre_predictions2

    for idx, thresh in enumerate(thresholds):
        f1 = np.empty(num_folds) # stores scores for respective metrics (f1, accuracy,precision,recall)
        acc = np.empty(num_folds)
        pre = np.empty(num_folds)
        rec = np.empty(num_folds)
        kf_iter = 0 # keeps track of terations through kf splits
        for train, test in kf.split(X):
            X_train = X.iloc[train]
            X_test = X.iloc[test]
            y_train = y.iloc[train]
            y_test = y.iloc[test]        

            primary_model.fit(X_train, y_train)
            y_prob = primary_model.predict_proba(X_test)
            y_pred = [1 if x >= thresh else 0 for x in y_prob[:, 1]] # changing values according th threshold

            f1[kf_iter] = f1_score(y_test, y_pred) # getting f1 and adding to numpy (f1)
            acc[kf_iter] = accuracy_score(y_test, y_pred) # getting f1 and adding to numpy (f1)
            pre[kf_iter] = precision_score(y_test, y_pred) # getting f1 and adding to numpy (f1)
            rec[kf_iter] = recall_score(y_test, y_pred) # getting f1 and adding to numpy (f1)
            kf_iter += 1


        results.iloc[idx, 0] = thresh
        results.iloc[idx, 1]= np.mean(f1)
        results.iloc[idx, 2]= np.mean(acc)
        results.iloc[idx, 3]= np.mean(pre)
        results.iloc[idx, 4]= np.mean(rec)

    return results

# tests ratios of composite model
def ratio_testing_composite(X, y, primary_model, preliminary_model1, preliminary_model2, threshold = .5, num_folds=5, iterations = 100):

    kf = KFold(n_splits=num_folds, shuffle=True)


    pre_predictions1 = pd.Series(index = X.index, dtype='float64') # Series to add the predictions from prelim models testing
    pre_predictions2 = pd.Series(index = X.index, dtype='float64')

    for train, test in kf.split(X):
        X_train = X.iloc[train]
        X_test = X.iloc[test]
        y_train = y.iloc[train]


        preliminary_model1.fit(X_train, y_train) # running through both models and adding to respective series
        prediction1 = preliminary_model1.predict_proba(X_test) 
        prediction1 = prediction1[:,1]
        pre_predictions1.iloc[test] = prediction1


        preliminary_model2.fit(X_train, y_train) 
        predictions2 = preliminary_model2.predict_proba(X_test) 
        predictions2 = predictions2[:,1]
        pre_predictions2.iloc[test] = predictions2



    X['prediction1'] = pre_predictions1 # add series to dataframe as columns
    X['prediction2'] = pre_predictions2


    return confusion_ratios(X,y,primary_model,threshold,iterations)





ada = AdaBoostClassifier(learning_rate=.021, n_estimators= 119)

logistic = LogisticRegression(l1_ratio=.075, max_iter=5000, penalty='elasticnet', solver='saga')

grad_boost = GradientBoostingClassifier(learning_rate=.042, max_depth=2, max_features=2, min_samples_leaf=9, min_samples_split=6, n_estimators=37, subsample=.3)

if __name__ == "__main__":
    X, y = read_in_return_Xy_no_time()

    for num in [.54,.55,.56,.57,.58,.59,.6]:
        print(ratio_testing_composite(X, y, grad_boost, logistic, ada, threshold=num, iterations = 1000))

    # {'thresh': 0.52, 'precision': 0.6418345219501103, 'npv': 0.5605746983751182, 'weighting': 0.7909957924263675}
    #  {'thresh': 0.53, 'precision': 0.6478468611540116, 'npv': 0.5500373183337923, 'weighting': 0.7500888265544647}
    # {'thresh': 0.54, 'precision': 0.6558876362507902, 'npv': 0.5449768798189758, 'weighting': 0.7123796166432913}
    # {'thresh': 0.55, 'precision': 0.6605514933812313, 'npv': 0.537370597278363, 'weighting': 0.6827723235156615}
    # {'thresh': 0.56, 'precision': 0.6666061050186906, 'npv': 0.5293085927762623, 'weighting': 0.6501309022907901}
    # {'thresh': 0.57, 'precision': 0.6738931852505924, 'npv': 0.5239213767619649, 'weighting': 0.6127676484338476}
    # {'thresh': 0.58, 'precision': 0.6790613282073099, 'npv': 0.5144410381437924, 'weighting': 0.5833800841514726}
    # {'thresh': 0.59, 'precision': 0.6891285702421535, 'npv': 0.5073728165137061, 'weighting': 0.5406965871902759}
    # {'thresh': 0.6, 'precision': 0.6913491970326614, 'npv': 0.4998425659645963, 'weighting': 0.5039504441327725}










    #print(composite_model(X, y, grad_boost, logistic, ada, num_folds=5))
    # ada.fit(X,y)
    # print(len(X))
    # print(ada.predict_proba(X)[:, 1])
    # print(len(ada.predict_proba(X)[:, 1]))
    # thresholds = [.51,.52,.53,.54, .55, .56,.57,.58,.59,.6,.61,.62,.63,.64,.65]
    # print(thresh_testing_composite(X, y, grad_boost, logistic, ada, thresholds))

    #    thresh        f1  accuracy precision    recall
    # 0    0.51  0.735967  0.622372  0.632404  0.881182
    # 1    0.52  0.730625  0.622371  0.637231  0.857055
    # 2    0.53   0.72094  0.625993  0.650581  0.808516
    # 3    0.54  0.717029  0.626225    0.6547  0.792624
    # 4    0.55  0.707452  0.625877  0.663596  0.757687
    # 5    0.56  0.702675   0.62436  0.666477  0.744152
    # 6    0.57  0.690694  0.620619  0.673943   0.70876
    # 7    0.58  0.681724  0.618748  0.680405  0.683327
    # 8    0.59  0.669314  0.614306  0.686527  0.653404
    # 9     0.6  0.643686  0.601215  0.690439  0.603081
    # 10   0.61  0.624716  0.594787  0.699632  0.564605
    # 11   0.62  0.584334  0.577841  0.710825  0.497192
    # 12   0.63   0.56524  0.570829  0.716823  0.467078
    # 13   0.64  0.534359  0.560776  0.729027  0.423154
    # 14   0.65   0.48104  0.539618  0.737695  0.357971
