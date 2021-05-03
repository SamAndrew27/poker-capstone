import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier

from load_df import read_in_holdout_return_X_y, read_in_training_return_Xy

plt.style.use('ggplot')
plt.rcParams.update({'font.size': 20})

def get_results(lower, upper):
    """Fits model with training data, predicts on holdout data. 
    Puts predictions/truth into dataframe. Changes predictions to 0 if they are above upper threshold, 1 if they are middle, and 2 if they are lower than 'lower'

    Args:
        lower (float): lowest threshold, everything below this always predicted as false
        upper (float): upper threshold, everything above this always predicted as positive

    Returns:
        2 arrays: one containing all the cases where I won/broke even and the other containing all cases where I lost
    """    
    X, y = read_in_training_return_Xy()
    X_holdout, y_holdout = read_in_holdout_return_X_y()

    gb_final = GradientBoostingClassifier(learning_rate=.01, n_estimators=90, min_samples_leaf=6 , min_samples_split=4 ,max_features= 3,max_depth= 5,subsample= .6)
    gb_final.fit(X,y)
    pred = gb_final.predict_proba(X_holdout)
    results = pd.DataFrame(data = {'truth': y_holdout, 'prediction': pred[:, 1]})

    results['prediction_category'] = results['prediction'].apply(lambda x: bin_predictions(x, lower, upper))
    won_mask = results['truth'] == 1
    won = results[won_mask]
    lost_mask = results['truth'] == 0
    lost = results[lost_mask]

    return won, lost


def bin_predictions(x, lower, upper):
    """categorizes predictions by thresholding prediction probas

    Args:
        x (prediction): float (predicted probability positive)
        lower (float): lower threshold, see 'get_results'
        upper (float): upper threshold, see 'get_results'

    Returns:
        [int]: 0 if above highest thresh, 1 if in middle, and 2 if below lower threshold 
    """    
    if x >= upper:
        return 0
    if x < upper and x > lower:
        return 1
    if x <= lower:
        return 2


def plot_results_3_categories(lower,upper):
    """plots results for 3 different categores (number won, number lost, percent of each)

    Args:
        lower (float): lower threshold, see 'get_results'
        upper (float): upper threshold, see 'get_results'

    Returns:
        ax: matplotlib ax containing plot 
    """    
    won, lost = get_results(lower,upper)
    won = won.prediction_category.value_counts().sort_index()
    lost = lost.prediction_category.value_counts().sort_index()

    won_percent = won / (won+lost)
    lost_percent = lost / (won+lost)

    q2_won = round(100 * won_percent[2], 1)
    q2_lost = round(100 * lost_percent[2], 1)
    q1_won = round(100 * won_percent[1], 1)
    q1_lost = round(100 * lost_percent[1], 1)
    q0_won = round(100 * won_percent[0], 1)
    q0_lost = round(100 * lost_percent[0], 1)

    labels = ['Play It!', "Caution", "Don't Do It!", ]

    print(won)
    print(won_percent)
    print(lost)
    print(lost_percent)

    fig, ax = plt.subplots(figsize=(20,20))

    width = 0.35
    x = np.arange(len(labels))
    won_ax = ax.bar(x=x - width/2, height= won, width=width, label="Won/Broke Even")
    lost_ax = ax.bar(x=x + width/2, height= lost, width=width, label="Lost")
    ax.set_ylabel('Number of Hands')
    ax.set_title('Number of Hands Won or Lost \n in Each Grouping')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    plt.text(x= .09, y = 40, s=f'{q0_lost}%', fontsize=20)
    plt.text(x= -.27, y = 40, s=f'{q0_won}%', fontsize=20)

    plt.text(x= 1.1, y = 40, s=f'{q1_lost}%', fontsize=20)
    plt.text(x= .75, y = 40, s=f'{q1_won}%', fontsize=20)

    plt.text(x= 2.1, y = 40, s=f'{q2_lost}%', fontsize=20)
    plt.text(x= 1.75, y = 40, s=f'{q2_won}%', fontsize=20)



    return ax 

if __name__=="__main__":
    # gb_final.fit(X,y)
    # pred = gb_final.predict_proba(X_holdout)
    # results = pd.DataFrame(data = {'truth': y_holdout, 'prediction': pred[:, 1]})

    

    # mask_highest = results['prediction'] >= 0.65
    # top_thresh = results[mask_highest]

    # mask_middle = (results['prediction'] < 0.65) & (results['prediction'] > 0.55)
    # middle_thresh = results[mask_middle] 
    # mask_middle = middle_thresh['prediction'] > 0.55
    # middle_thresh = middle_thresh[mask_middle] 

    # bottom_mask = results['prediction'] <= 0.55
    # bottom_thresh = results[bottom_mask]
    # won, lost = get_results()
    # won = won.prediction_category.value_counts().sort_index()
    # lost = lost.prediction_category.value_counts().sort_index()

    # won_percent = won / (won+lost)
    # lost_percent = lost / (won+lost)
    # bottom_won = round(100 * won_percent["Don't Do It!"], 1)
    # print(bottom_won)
    ax = plot_results_3_categories(.53,.62)
    plt.show()