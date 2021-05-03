import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
import seaborn as sns 

from load_df import join_training_holdout

plt.style.use('ggplot')
plt.rcParams.update({'font.size': 20})

def plot_card_rank_sns(): 
    """plots card_rank with seaborn histogram

    Returns:
        ax: matplotlib ax with results plotted 
    """    
    df = join_training_holdout()
    fig, ax = plt.subplots(figsize=(20,20))
    df['Outcome'] = df['made_or_lost'].apply(lambda x: give_names(x))
    ax = sns.histplot(data=df, x='card_rank', hue='Outcome', bins=20, element='step', hue_order=['Won/Broke Even', 'Lost'])
    ax.set_xlabel('Card Rank')
    

    ax.set_ylabel('Number of Hands')
    ax.set_title('Number of Hands Won or Lost \n by Card Rank')
    return ax 


def give_names(x):
    """changes values in 'made_or_lost' from int to strings

    Args:
        x: 'made_or_lost'

    Returns:
        string: 'Lost' if 0, 'Won/Broke Even' if 1
    """    
    if x == 0:
        return 'Lost'
    else:
        return 'Won/Broke Even'

if __name__ == "__main__":

    ax1 = plot_card_rank_sns()



    plt.show()