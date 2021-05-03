import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier

from load_df import join_training_holdout

plt.style.use('ggplot')
plt.rcParams.update({'font.size': 12})


# TABLING THIS FOR NOW!!!

''' MAYBE RETURN TO THIS???
def feature_importance(model, X, y):
    cols = list(X.columns)
    results = pd.Series(index=cols)
    model.fit(X,y)

    for idx, num in enumerate(model.feature_importances_):
        results.loc[cols[idx]] = num
    
    fig, ax = plt.subplots()

    lil_x = np.arange(len(cols))

    ax.bar(x=lil_x, height=results)
    ax.set_xticks(lil_x)
    ax.set_xticklabels(cols)    
    return ax
'''
def feature_importance(model, X, y):
    result = pd.Series(index=list(X.columns))
    cols = list(X.columns)

    model.fit(X,y)
    for idx, num in enumerate(model.feature_importances_):
        result.loc[cols[idx]] = num * 100
    return result 



if __name__=="__main__":
    X,y = join_training_holdout(target=True)
    X.columns = ['suited',
            'low_card',
            'position',
            'high_card',
            'card_rank',
            'limpers', 
            'raises',
            'players_before',
            'players_after',
            'BB_in_stack']
    # y = df['made_or_lost']
    # X =  df[['suited',
    #         'low_card',
    #         'position',
    #         'high_card',
    #         'card_rank',
    #         'limpers', 
    #         'raises&reraises',
    #         'num_players_before',
    #         'num_players_after',
    #         'BB_in_stack']]

    gb_final = GradientBoostingClassifier(learning_rate=.01, n_estimators=90, min_samples_leaf=6 , min_samples_split=4 ,max_features= 3,max_depth= 5,subsample= .6)

    result = feature_importance(gb_final, X, y).sort_values()
    print(result)
    ax = result.plot.bar()
    plt.xticks(rotation=35)
    ax.set_ylabel('Percentage of Importance')
    ax.set_title('Feature Importance Plot')
    # plt.legend()
    plt.show()
