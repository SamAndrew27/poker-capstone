import seaborn as sns 
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
from load_df import load_whole
plt.style.use('ggplot')



def plot_raises():
    won, lost, __ = load_whole()
    won['raises&reraises'] = won['raises&reraises'].apply(lambda x: change_raise(x))
    lost['raises&reraises'] = lost['raises&reraises'].apply(lambda x: change_raise(x))

    fig, ax = plt.subplots()
    width = 0.35
    labels = ['Raised','Unraised']
    x = np.arange(len(labels))
    won_ax = ax.bar(x=x - width/2, height= won['raises&reraises'].value_counts(), width=width, label='won')
    lost_ax = ax.bar(x=x + width/2, height= lost['raises&reraises'].value_counts(), width=width, label='lost')
    ax.legend()
    ax.set_xticks(x)
    ax.set_xticklabels(labels)

    ax.set_ylabel('Number of Hands')
    ax.set_title('Number of Hands Won or Lost \n by Whether Pot was Raise')
    return ax 


def change_raise(x):
    '''
    groups raises by 1+ vs 0
    for lambda function above
    '''
    if x > 0:
        return 'raised pot'
    else:
        return 'no raise'

if __name__ == "__main__":
    ax = plot_raises()
    plt.show()