from load_df import load_whole
import seaborn as sns 
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
plt.style.use('ggplot')
plt.rcParams.update({'font.size': 20})


# def plot_card_rank(): # probably could use some cleanup 
#     _, _,df = load_whole()
#     fig, ax = plt.subplots()
#     ax = sns.kdeplot(data=df, x='card_rank', hue='made_or_lost', fill=True)
#     ax.legend(['won', 'lost'])
#     return ax 

# keep playing with this one, run it by DSR/instructor
def plot_card_rank_sns(setup='stack'): # consider changing to offset (rather than stacked barchart)
    won, lost, df = load_whole()
    fig, ax = plt.subplots(figsize=(20,20))
    # cmap = sns.cm.rocket_r
    df['Outcome'] = df['made_or_lost'].apply(lambda x: give_names(x))
    ax = sns.histplot(data=df, x='card_rank', hue='Outcome', bins=20, element='step', hue_order=['Made Money/Broke Even', 'Lost Money'])
    ax.set_xlabel('Card Rank')
    
    # ax.legend()

    ax.set_ylabel('Number of Hands')
    ax.set_title('Number of Hands Won or Lost \n by Card Rank')
    return ax 

def card_rank_bar():
    won, lost, df = load_whole()
    labels = sorted(list(df['card_rank'].unique()))
    x = np.arange(len(labels))
    width = 0.35
    fig, ax = plt.subplots()
    won_ax = ax.bar(x - width/2, won['card_rank'].value_counts().sort_index(), width=width, label='won')
    lost_ax = ax.bar(x + width/2, lost['card_rank'].value_counts().sort_index(), width=width, label='lost')

    return ax

def card_rank_violin():
    fig, ax = plt.subplots()

    won, lost, df = load_whole()
    ax = sns.violinplot(data=df, x='made_or_lost', y='card_rank')
    
    return ax 

def give_names(x):
    if x == 0:
        return 'Lost Money'
    else:
        return 'Made Money/Broke Even'

if __name__ == "__main__":

    ax1 = plot_card_rank_sns()
    # ax2 = plot_card_rank_sns(setup='dodge')

    # ax2 = card_rank_bar()
    # ax3 = card_rank_violin()




    plt.show()