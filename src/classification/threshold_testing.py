from sklearn.ensemble import GradientBoostingClassifier
from capstone3_data_prep import training_data_Xy
import pandas as pd 
import numpy as np 
from grid_and_thresh_funcs import threshold_testing, confusion, confusion_ratios
from sklearn.model_selection import KFold
import matplotlib.pyplot as plt 
plt.style.use('ggplot')
import seaborn as sns 



gb_final = GradientBoostingClassifier(learning_rate=.01, n_estimators=90, min_samples_leaf=6 , min_samples_split=4 ,max_features= 3,max_depth= 5,subsample= .6)


X, y = read_in_return_Xy_no_unused()


def test_prediction_results(X, y, model, num_folds=5):
    """does cv to get predictions for entire dataframe

    Args:
        X (array): features
        y (array): target
        model (sklearn model): model to be tested
        num_folds (int, optional): number of folds in cross val. Defaults to 5.

    Returns:
        [type]: [description]
    """    
    kf = KFold(n_splits=num_folds, shuffle=True)
    results = pd.DataFrame(columns=['prediction', 'truth'], index=X.index)
    for train, test in kf.split(X):
        X_train = X.iloc[train]
        X_test = X.iloc[test]
        y_train = y.iloc[train]
        y_test = y.iloc[test]    

        model.fit(X_train, y_train)
        y_prob = model.predict_proba(X_test)

        results['prediction'].iloc[test] = y_prob[:, 1]
        results['truth'].iloc[test] = y_test



    return results

def test_results(results, upperbound, lowerbound):
    """gets dataframe of predictions/target, gets subset of that dataframe bounded by two thresholds, returns portion of that dataframe that is actually true

    Args:
        results (dataframe): contains predictions/actual values
        upperbound (float): upper bound of prediction threshold
        lowerbound (flaot): lowerbound of prediction threshold

    Returns:
        float: number of positive cases in subsection considered divided by length of subsection considered 
    """    
    # results = results.mask((results['prediction'] <= upperbound) & (results['prediction'] >= lowerbound))
    upper_mask = results['prediction'] <= upperbound
    results = results[upper_mask]
    lower_mask = results['prediction'] > lowerbound
    results = results[lower_mask]

    result = np.sum(results['truth']) / len(results)
    return result


if __name__=="__main__":

    thresholds = [.5,.51,.52,.53,.54,.55,.56,.57,.58,.59,.6,.61,.62,.63,.64,.65,.66,.67]

    # print(threshold_testing(X,y,gb_final, thresholds))
    #    thresh        f1  accuracy precision    recall
    # 0     0.5  0.761121  0.645512  0.637658  0.944031
    # 1    0.51  0.761108  0.649369  0.642448  0.933603
    # 2    0.52  0.757732  0.649838  0.646678  0.915687
    # 3    0.53  0.757227  0.654511  0.653304  0.900583
    # 4    0.54  0.753532  0.657437  0.661757   0.87591
    # 5    0.55  0.748956  0.659071  0.669358  0.850221
    # 6    0.56  0.748318  0.666786  0.682832  0.828662
    # 7    0.57  0.740537  0.667602  0.694593  0.793347
    # 8    0.58   0.72442  0.657665  0.698846   0.75282
    # 9    0.59  0.700385  0.645864  0.709397  0.692694
    # 10    0.6  0.679033  0.637566  0.722905  0.641611
    # 11   0.61  0.653304  0.626111  0.733337   0.58965
    # 12   0.62  0.621514  0.609398  0.739189  0.536491
    # 13   0.63  0.593634  0.597243  0.749342  0.492053
    # 14   0.64  0.554329  0.579358  0.757746  0.438632
    # 15   0.65  0.508505  0.561829  0.773079  0.379616
    # 16   0.66  0.438114  0.534597  0.788436  0.303896
    # 17   0.67  0.365839  0.509467  0.807476   0.23677
    thresh = .59
    # print(confusion_ratios(X,y,gb_final, thresh, 10))
    # print(confusion(X,y,gb_final, thresh))

    # results = test_prediction_results(X, y, gb_final) 
    # print(test_results(results, .55, .53))
    print(X.info())

    
    # .65+ seems good for must play
    # .55-.65 for maybe play? 
    # .55- seems good for don't play 
    # ax = sns.histplot(data=results, x='prediction', hue='truth')
    # plt.show()
    