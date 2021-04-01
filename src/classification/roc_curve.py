import pandas as pd 
import numpy as np 
from sklearn.metrics import roc_curve, auc
from class_prep import read_in_holdout_no_time, read_in_return_Xy_no_time
import matplotlib.pyplot as plt 
from class_prep import read_in_holdout_no_time, read_in_return_Xy_no_time
from sklearn.ensemble import GradientBoostingClassifier


grad_boost = GradientBoostingClassifier(learning_rate=.042, max_depth=2, max_features=2, min_samples_leaf=9, min_samples_split=6, n_estimators=37, subsample=.3)
X, y = read_in_return_Xy_no_time()
X_holdout, y_holdout = read_in_holdout_no_time()


def plot_roc(model, X, y, X_holdout, y_holdout, threshold, savefig=False):
    model.fit(X,y)

    y_prob = model.predict_proba(X_holdout)
    y_pred = [1 if x >= threshold else 0 for x in y_prob[:, 1]] 

    fpr, tpr, threshold = roc_curve(y_holdout, y_pred)
    roc_auc = auc(fpr,tpr)


    fig, ax = plt.subplots(figsize=(12,12))

    plt.title('Gradient Boost ROC - Threshold:.58')
    ax.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
    ax.legend(loc = 'lower right')
    ax.plot([0, 1], [0, 1],'r--')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    if savefig:
        plt.savefig('roc_curve.png', dpi=fig.dpi)
    else:
        plt.show()



if __name__ == "__main__":
    plt.rcParams.update({'font.size': 18})

    plot_roc(grad_boost, X, y, X_holdout, y_holdout, threshold = .58, savefig=True)