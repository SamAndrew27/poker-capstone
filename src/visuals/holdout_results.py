import seaborn as sns 
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
from load_df import load_whole, read_in_holdout_return_X_y, read_in_return_Xy_no_unused
from sklearn.ensemble import GradientBoostingClassifier
plt.style.use('ggplot')
plt.rcParams.update({'font.size': 15})

def get_results():
    X, y = read_in_return_Xy_no_unused()
    X_holdout, y_holdout = read_in_holdout_return_X_y()

    gb_final = GradientBoostingClassifier(learning_rate=.01, n_estimators=90, min_samples_leaf=6 , min_samples_split=4 ,max_features= 3,max_depth= 5,subsample= .6)
    gb_final.fit(X,y)
    pred = gb_final.predict_proba(X_holdout)
    results = pd.DataFrame(data = {'truth': y_holdout, 'prediction': pred[:, 1]})

    results['prediction_category'] = results['prediction'].apply(lambda x: bin_predictions(x))
    won_mask = results['truth'] == 1
    won = results[won_mask]
    lost_mask = results['truth'] == 0
    lost = results[lost_mask]

    return won, lost

def bin_predictions(x):
    if x >= .65:
        return 'Play It!'
    if x < .65 and x > .55:
        return 'Maybe?'
    if x <= .55:
        return "Don't Do It!"

def plot_results():
    won, lost = get_results()
    won = won.prediction_category.value_counts().sort_index()
    lost = lost.prediction_category.value_counts().sort_index()

    won_percent = won / (won+lost)
    lost_percent = lost / (won+lost)
    bottom_won = round(100 * won_percent["Don't Do It!"], 1)
    bottom_lost = round(100 * lost_percent["Don't Do It!"], 1)
    middle_won = round(100 * won_percent["Maybe?"], 1)
    middle_lost = round(100 * lost_percent["Maybe?"], 1)
    top_won = round(100 * won_percent['Play It!'], 1)
    top_lost = round(100 * lost_percent['Play It!'], 1)

    labels = ["Don't Do It!", 'Consider Playing', 'Play It!']




    fig, ax = plt.subplots()

    width = 0.35
    x = np.arange(len(labels))
    won_ax = ax.bar(x=x - width/2, height= won, width=width, label="Won")
    lost_ax = ax.bar(x=x + width/2, height= lost, width=width, label="lost")
    ax.set_ylabel('Number of Hands')
    ax.set_title('Number of Hands Won or Lost \n in Each Grouping')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)

    plt.text(x= -.335, y = 90, s=f'{bottom_won}%', fontsize=12)
    plt.text(x= .02, y = 90, s=f'{bottom_lost}%', fontsize=12)

    plt.text(x= .68, y = 90, s=f'{middle_won}%', fontsize=12)
    plt.text(x= 1.03, y = 90, s=f'{middle_lost}%', fontsize=12)

    plt.text(x= 1.67, y = 90, s=f'{top_won}%', fontsize=12)
    plt.text(x= 2.02, y = 90, s=f'{top_lost}%', fontsize=12)
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
    ax = plot_results()
    plt.show()