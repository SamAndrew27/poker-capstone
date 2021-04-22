import seaborn as sns 
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
plt.style.use('ggplot')
from load_df import won_lost_for_BB

# def plot_bb():
#     _, _,df = load_whole()
#     fig, ax = plt.subplots()
#     ax = sns.kdeplot(data=df, x='BB_in_stack', hue='made_or_lost', fill=True)
#     # ax.set(xlim=(0,100))
#     ax.legend(['won','lost'])
#     return ax 


# maybe cut these off at 100 instead of 200?
def bb_plot_sns(rounded = None, cutoff=200):
    _, _, df = won_lost_for_BB(rounded, cutoff)

    fig, ax = plt.subplots()



    ax = sns.histplot(data=df, x='BB_in_stack', hue='made_or_lost', multiple='dodge', element='step')
    return ax 

def bb_violin(rounded=None, cutoff=200):
    _, _, df = won_lost_for_BB(rounded, cutoff)

    fig, ax = plt.subplots()

    ax = sns.violinplot(data=df, x='made_or_lost', y='BB_in_stack')

    return ax 

def bb_bar(rounded=5, cutoff=120):
    won, lost, df = won_lost_for_BB(rounded, cutoff)
    labels = sorted(list(df['BB_in_stack'].unique()))

    x = np.arange(len(labels))
    width = 0.35
    fig, ax = plt.subplots()

    won_ax = ax.bar(x - width/2, won['BB_in_stack'].value_counts(), width=width, label='won')
    lost_ax = ax.bar(x + width/2, lost['BB_in_stack'].value_counts(), width=width, label='lost')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel('Number of Hands')
    ax.set_xlabel('BB in Stack')

    ax.set_title('Number of Hands Won or Lost \n by BB in Stack')
    return ax

    


if __name__ == "__main__":
    # ax1 = bb_plot_sns(rounded = 5, cutoff=100)


    # ax2 = bb_plot_sns(rounded = 1, cutoff=100) # CONSIDER USING THIS ONE
    
    
    # ax3 = bb_plot_sns(rounded = 10, cutoff=100)
    # ax4 = bb_plot_sns(rounded = 5, cutoff=200)
    # ax5 = bb_violin(cutoff=200)
    # ax6 = bb_violin(cutoff=100)

    ax7 = bb_bar(rounded=5, cutoff=100)
    # ax8 = bb_bar(rounded=10, cutoff=150)
    # ax9 = bb_bar(rounded=10, cutoff=100)

    plt.show()