from load_df import load_whole
import seaborn as sns 
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier

plt.style.use('ggplot')
plt.rcParams.update({'font.size': 15})


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
    cols = list(X.columns)

    model.fit(X,y)
    for idx, num in enumerate(model.feature_importances_):
        print(f'{cols[idx]}:{num}')

if __name__=="__main__":
    _, _, df = load_whole()

    y = df['made_or_lost']
    X =  df[['suited',
            'low_card',
            'position',
            'high_card',
            'card_rank',
            'limpers', 
            'raises&reraises',
            'num_players_before',
            'num_players_after',
            'BB_in_stack']]

    gb_final = GradientBoostingClassifier(learning_rate=.01, n_estimators=90, min_samples_leaf=6 , min_samples_split=4 ,max_features= 3,max_depth= 5,subsample= .6)

    print(feature_importance(gb_final, X, y))

