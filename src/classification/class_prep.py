import pandas as pd 
import numpy as np 
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV, train_test_split, KFold
from sklearn.metrics import f1_score, confusion_matrix, accuracy_score, recall_score, precision_score

#split into two

def read_in_holdout_no_time():
    X = pd.read_csv('/home/sam/Documents/DSI/capstone/poker/data/holdout_classification_tournaments.csv')
    X = X.drop(X.columns[0], axis = 1)
    y = X['made_or_lost']
    X =  X.drop(['made_or_lost', 'hour', 'days_since_start', 'hand_frequency'], axis = 1)
    return X, y 

def read_in_data():
    df = pd.read_csv('/home/sam/Documents/DSI/capstone/poker/data/train_classification_tournaments.csv')
    df = df.drop(df.columns[0], axis = 1)

    return df

def read_in_return_Xy():
    X = read_in_data()


    y = X['made_or_lost']
    del X['made_or_lost']

    return X, y 

def read_in_return_Xy_no_time():
    X = read_in_data()
    y = X['made_or_lost']

    X =  X.drop(['made_or_lost', 'hour', 'days_since_start', 'hand_frequency'], axis = 1)

    return X, y 

def read_in_return_X_scaled():
    X = read_in_data()
    y = X['made_or_lost']
    del X['made_or_lost']

    SS = StandardScaler()
    X = pd.DataFrame(data = SS.fit_transform(X), columns = list(X.columns))    

    return X, y

def read_in_return_X_scaled_no_time():
    X = read_in_data()
    y = X['made_or_lost']
    X =  X.drop(['made_or_lost', 'hour', 'days_since_start', 'hand_frequency'], axis = 1)

    SS = StandardScaler()
    X = pd.DataFrame(data = SS.fit_transform(X), columns = list(X.columns))    

    return X, y

def grid_search(X, y, model, param_grid, return_stuff = False):
    
    gscv = GridSearchCV(estimator= model, param_grid=param_grid, n_jobs = -1, verbose=1, scoring='f1')

    gscv.fit(X, y)



    if return_stuff:
        return gscv.best_estimator_, gscv.best_score_
    else:
        print(gscv.best_estimator_)
        print(gscv.best_score_)   




def X_y_train_test():
    X = read_in_data()
    y = X['made_or_lost']
    X =  X.drop(['made_or_lost', 'hour', 'days_since_start', 'hand_frequency'], axis = 1)
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    return X_train, X_test, y_train, y_test


########################################################################

def threshold_testing(X, y, model,thresholds, num_folds=5):

    results = pd.DataFrame(columns=['thresh', 'f1', 'accuracy', 'precision','recall'],index=list(range(0, len(thresholds)))) # stores the results of all theshold tests
    kf = KFold(n_splits=num_folds, shuffle=True)
    for idx, thresh in enumerate(thresholds):
        kf_iter = 0 # counts iterations through kf split, for use in indexing into numpy f1
        f1 = np.empty(num_folds) # stores scores for respective metrics (f1, accuracy,precision,recall)
        acc = np.empty(num_folds)
        pre = np.empty(num_folds)
        rec = np.empty(num_folds)

        for train, test in kf.split(X):
            X_train = X.iloc[train]
            X_test = X.iloc[test]
            y_train = y.iloc[train]
            y_test = y.iloc[test]     

            model.fit(X_train, y_train)
            y_prob = model.predict_proba(X_test)
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

def confusion(X,y,model,threshold):
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    model.fit(X_train,y_train)
    y_prob = model.predict_proba(X_test)
    y_pred = [1 if x >= threshold else 0 for x in y_prob[:, 1]] # changing values according th threshold
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    result = {'TP': tp, 'FP': fp, 'TN': tn, 'FN': fn}
    return result

#rather than coding out something better (using metrics) Im just going to run this a bunch of times to come to a conclusion about which model is better
#sorry, sh
def confusion_ratios(X,y,model,threshold, iterations = 100): # specific ratios i'm looking at
    pre_lst = []
    npv_lst = []
    weight_lst = []
    for num in range(iterations):
        confusion_dic = confusion(X,y,model,threshold)
        # precision done by hand, followed by NPV done by hand
        precision = confusion_dic['TP'] / (confusion_dic['FP'] + confusion_dic['TP'])
        npv =  confusion_dic['TN'] / ( confusion_dic['TN'] + confusion_dic['FN'])
        # ratio positive, ideally about 60%, pretty sure theres a metric for this as well but whatever i like wasting time i guess
        weighting = (confusion_dic['TP'] + confusion_dic['FP'] )/ (confusion_dic['TP'] + confusion_dic['FP'] + confusion_dic['TN'] + confusion_dic['FN'] ) 
        pre_lst.append(precision)
        npv_lst.append(npv)
        weight_lst.append(weighting)

    average = {'thresh': thresh, 'precision': np.mean(pre_lst), 'npv': np.mean(npv_lst), 'weighting': np.mean(weight_lst)}


    return average

if __name__ == "__main__":
    thresholds = [.1,.2,.3,.4,.5,.6,.7,.8,.9]

