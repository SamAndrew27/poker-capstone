import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd

from load_df import split_won_lost

plt.style.use('ggplot')
plt.rcParams.update({'font.size': 20})


def plot_raises():
    """plots whether I won or lost according to number of raises

    Returns:
        ax: matplotlib ax with plot on it
    """    
    won, lost, __ = split_won_lost()
    won['raises&reraises'] = won['raises&reraises'].apply(lambda x: change_raise(x))
    lost['raises&reraises'] = lost['raises&reraises'].apply(lambda x: change_raise(x))

    fig, ax = plt.subplots()
    width = 0.35
    labels = ['Unraised', 'Raised']
    x = np.arange(len(labels))
    won_ax = ax.bar(x=x - width/2, height= won['raises&reraises'].value_counts(), width=width, label='Won/Broke Even')
    lost_ax = ax.bar(x=x + width/2, height= lost['raises&reraises'].value_counts(), width=width, label='Lost')
    ax.legend()
    ax.set_xticks(x)
    ax.set_xticklabels(labels)

    ax.set_ylabel('Number of Hands')
    ax.set_title('Number of Hands Won or Lost \n by Whether Pot was Raise')
    return ax 


def change_raise(x):
    """groups raises into 2 categories, cases where there was a raise and cases there was not

    Args:
        x : 'raises&reraises' column this is being applied to. x should be an int 

    Returns:
        string: 'raised pot' if value is 1+, otherwise 'no raise' 
    """    

    if x > 0:
        return 'raised pot'
    else:
        return 'no raise'

if __name__ == "__main__":
    ax = plot_raises()

    # won, lost, __ = load_whole()
    # won['raises&reraises'] = won['raises&reraises'].apply(lambda x: change_raise(x))
    # lost['raises&reraises'] = lost['raises&reraises'].apply(lambda x: change_raise(x))
    # print(won['raises&reraises'].value_counts())
    # print(lost['raises&reraises'].value_counts())

    plt.show()
