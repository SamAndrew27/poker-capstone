import pandas as pd 
import numpy as np 
from sklearn.metrics import roc_curve, auc, plot_roc_curve
import matplotlib.pyplot as plt 
from sklearn.ensemble import GradientBoostingClassifier
from load_df import read_in_training_return_Xy

model = GradientBoostingClassifier(learning_rate=.01, n_estimators=90, min_samples_leaf=6 , min_samples_split=4 ,max_features= 3,max_depth= 5,subsample= .6)

X, y = read_in_training_return_Xy()

def plot_roc_non_thresh(model, X, y, savefig=False):
    """Plots roc_curve for data

    Args:
        model: model to be used to determine roc
        X (array): features
        y (array): target
        savefig (bool, optional): If True saves figure, otherwise displays figure. Defaults to False.
    """    

    model.fit(X,y)
    plot_roc_curve(model, X, y)
    plt.plot([0, 1], [0, 1],'r--')
    plt.legend("")
    plt.title('ROC Curve of Model')
    if savefig:
        plt.savefig('roc_curve.png', dpi=fig.dpi)
    else:
        plt.show()


if __name__=="__main__":
    plot_roc_non_thresh(model, X,y)