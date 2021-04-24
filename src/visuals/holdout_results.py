import seaborn as sns 
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
from load_df import load_whole, read_in_holdout_return_X_y, read_in_return_Xy_no_unused
from sklearn.ensemble import GradientBoostingClassifier
plt.style.use('ggplot')
plt.rcParams.update({'font.size': 20})

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

# def bin_predictions(x):
#     if x >= .655:
#         return 'Play It!'
#     if x < .65 and x > .595:
#         return 'Probably Win'
#     if x <= .595 and x > .51:
#         return 'Caution Zone'
#     if x <= .51:
#         return "Don't Do It!"

def bin_predictions(x):
    if x >= .655:
        return 0
    if x < .65 and x > .595:
        return 1
    if x <= .595 and x > .51:
        return 2
    if x <= .51:
        return 3

def plot_results():
    won, lost = get_results()
    won = won.prediction_category.value_counts().sort_index()
    lost = lost.prediction_category.value_counts().sort_index()

    won_percent = won / (won+lost)
    lost_percent = lost / (won+lost)

    q3_won = round(100 * won_percent[3], 1)
    q3_lost = round(100 * lost_percent[3], 1)  
    q2_won = round(100 * won_percent[2], 1)
    q2_lost = round(100 * lost_percent[2], 1)
    q1_won = round(100 * won_percent[1], 1)
    q1_lost = round(100 * lost_percent[1], 1)
    q0_won = round(100 * won_percent[0], 1)
    q0_lost = round(100 * lost_percent[0], 1)

    labels = ['Play It!', 'Probable Win', "Caution Zone", "Don't Do It!", ]




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

    plt.text(x= .06, y = 40, s=f'{q0_lost}%', fontsize=20)
    plt.text(x= -.3, y = 40, s=f'{q0_won}%', fontsize=20)

    plt.text(x= 1.05, y = 40, s=f'{q1_lost}%', fontsize=20)
    plt.text(x= .7, y = 40, s=f'{q1_won}%', fontsize=20)

    plt.text(x= 2.05, y = 40, s=f'{q2_lost}%', fontsize=20)
    plt.text(x= 1.7, y = 40, s=f'{q2_won}%', fontsize=20)

    plt.text(x= 3.05, y = 40, s=f'{q3_lost}%', fontsize=20)
    plt.text(x= 2.7, y = 40, s=f'{q3_won}%', fontsize=20)

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