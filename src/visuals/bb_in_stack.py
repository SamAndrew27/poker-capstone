import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd

from load_df import won_lost_for_BB

plt.style.use('ggplot')
plt.rcParams.update({'font.size': 20})


def bb_bar(rounded=5, cutoff=120):
    """creates bar plot for BB_in_stack. 

    Args:
        rounded (int, optional): Number to round BB_in_stack values to. Defaults to 5.
        cutoff (int, optional): Highest value of BB_in_stack considered for plotting. Defaults to 120.

    Returns:
        ax: matplotlib ax containing plot 
    """    
    won, lost, df = won_lost_for_BB(rounded, cutoff)
    labels = sorted(list(df['BB_in_stack'].unique()))

    x = np.arange(len(labels))
    width = 0.35
    fig, ax = plt.subplots(figsize=(20,20))

    won_ax = ax.bar(x - width/2, won['BB_in_stack'].value_counts().sort_index(), width=width, label='Won/Broke Even')
    lost_ax = ax.bar(x + width/2, lost['BB_in_stack'].value_counts().sort_index(), width=width, label='Lost')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel('Number of Hands')
    ax.set_xlabel('BB in Stack')
    ax.legend()

    ax.set_title('Number of Hands Won or Lost \n by BB in Stack')
    return ax

    


if __name__ == "__main__":


    ax7 = bb_bar(rounded=5, cutoff=100)

    plt.show()