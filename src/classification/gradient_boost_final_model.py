import pandas as pd 
import numpy as np 
from sklearn.metrics import f1_score, confusion_matrix, accuracy_score, recall_score, precision_score, brier_score_loss, roc_auc_score
from class_prep import read_in_holdout_no_time, read_in_return_Xy_no_time
import matplotlib.pyplot as plt 
from sklearn.ensemble import GradientBoostingClassifier

grad_boost = GradientBoostingClassifier(learning_rate=.042, max_depth=2, max_features=2, min_samples_leaf=9, min_samples_split=6, n_estimators=37, subsample=.3)
X, y = read_in_return_Xy_no_time()
X_holdout, y_holdout = read_in_holdout_no_time()

def test_holdout(model, X, y, X_holdout, y_holdout, threshold):
    results = {}

    model.fit(X,y)

    y_prob = model.predict_proba(X_holdout)
    y_pred = [1 if x >= threshold else 0 for x in y_prob[:, 1]]


    tn, fp, fn, tp = confusion_matrix(y_holdout, y_pred).ravel()

    results['npv'] = tn / (tn + fn)
    results['f1'] = f1_score(y_holdout, y_pred)
    results['accuracy'] = accuracy_score(y_holdout, y_pred)
    results['precision'] = precision_score(y_holdout, y_pred)
    results['recall'] = recall_score(y_holdout, y_pred)
    results['brier'] = brier_score_loss(y_holdout, y_pred)
    results['roc_auc'] = roc_auc_score(y_holdout, y_pred)


    return results, tn, fp, fn, tp 

def test_holdout_average(model, X, y, X_holdout, y_holdout, threshold, num_iterations=100):
    nvp = []
    f1 = []
    accuracy = []
    precision = []
    recall = []
    brier = []
    roc_auc = []
    tn_lst = []
    fp_lst = []
    fn_lst = []
    tp_lst = []
   
    for num in range(num_iterations):
        results, tn, fp, fn, tp = test_holdout(model, X, y, X_holdout, y_holdout, threshold=.58)
        nvp.append(results['npv'])
        f1.append(results['f1'])
        accuracy.append(results['accuracy'])
        precision.append(results['precision'])
        recall.append(results['recall'])
        brier.append(results['brier'])
        roc_auc.append(results['roc_auc'])

        tn_lst.append(tn)
        fp_lst.append(fp)
        fn_lst.append(fn)
        tp_lst.append(tp)

    return np.mean(nvp), np.mean(f1), np.mean(accuracy), np.mean(precision), np.mean(recall), np.mean(brier), np.mean(roc_auc), np.mean(tn_lst), np.mean(fp_lst), np.mean(fn_lst), np.mean(tp_lst), 
        
if __name__ == "__main__":

    print(test_holdout_average(grad_boost, X, y, X_holdout, y_holdout, threshold = .58, num_iterations= 1000))
    # print(X.info())
    # print(grad_boost.feature_importances_)
    # print(np.mean(y_holdout))


    # 1st test
    # (0.5416149068322982, 0.6985097439816584, 0.6311360448807855, 0.7123928293063133, 0.3688639551192146, 0.6108693118494184, 436.0, 420.0, 369.0, 914.0)
 
    # 1000 iterations:
    # (0.5318260613237492, 0.6887608697892491, 0.6247985039738196, 0.6923382696804365, 0.37520149602618047, 0.6079530133448912, 448.174, 407.826, 394.73, 888.27)
