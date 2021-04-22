import seaborn as sns 
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
from load_df import load_whole, won_lost_for_num_players
plt.style.use('ggplot')



def plot_num_players_under3():
    won, lost ,_ = load_whole()
    mask = won['num_players_before'] < 3
    won = won[mask]
    mask = lost['num_players_before'] < 3
    lost = lost[mask]
    width = 0.35
    fig, ax = plt.subplots()
    labels = ['0','1','2']
    x = np.arange(len(labels))
    won_ax = ax.bar(x=x - width/2, height= won['num_players_before'].value_counts(), width=width, label='won')
    lost_ax = ax.bar(x=x + width/2, height= lost['num_players_before'].value_counts(), width=width, label='lost')
    ax.legend()
    ax.set_xticks(x)
    ax.set_xticklabels(labels)

    ax.set_ylabel('Number of Hands')
    ax.set_xlabel('Number of Players Who Entered Pot Before Me')
    ax.set_title('Number of Hands Won or Lost \n by Number of Players to Enter Pot')

    return ax 

def plot_num_players_over3():
    won, lost ,_ = load_whole()

    mask = won['num_players_before'] >= 3
    won = won[mask]    
    mask = lost['num_players_before'] >= 3
    lost = lost[mask]   

    fig, ax = plt.subplots()

    width = 0.35
    labels = ['3','4','5']
    x = np.arange(len(labels))
    won_ax = ax.bar(x=x - width/2, height= won['num_players_before'].value_counts(), width=width, label='won')
    lost_ax = ax.bar(x=x + width/2, height= lost['num_players_before'].value_counts(), width=width, label='lost')
    ax.legend()
    ax.set_xticks(x)
    ax.set_xticklabels(labels)

    ax.set_ylabel('Number of Hands')
    ax.set_xlabel('Number of Players Who Entered Pot Before Me')
    ax.set_title('Number of Hands Won or Lost \n by Number of Players to Enter Pot')

    return ax 

def plot_together():
    won, lost, _ = won_lost_for_num_players()

    fig, ax = plt.subplots()


    width = 0.35
    labels = ['0','1','2+']
    x = np.arange(len(labels))
    won_ax = ax.bar(x=x - width/2, height= won['num_players_before'].value_counts(), width=width, label='won')
    lost_ax = ax.bar(x=x + width/2, height= lost['num_players_before'].value_counts(), width=width, label='lost')
    ax.legend()
    ax.set_xticks(x)
    ax.set_xticklabels(labels)

    ax.set_ylabel('Number of Hands')
    ax.set_xlabel('Number of Players Who Entered Pot Before Me')
    ax.set_title('Number of Hands Won or Lost \n by Number of Players to Enter Pot')

    return ax 

if __name__=="__main__":
    # ax1 = plot_num_players_under3()
    # ax2 = plot_num_players_over3()
    ax3 = plot_together()
    plt.show()