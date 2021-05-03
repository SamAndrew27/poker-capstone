import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd

from load_df import won_lost_for_num_players

plt.style.use('ggplot')
plt.rcParams.update({'font.size': 20})




def plot_together():
    """plots the number of players in the hand versus whether I won or lost (bars for each)

    Returns:
        ax: matplotlib ax containing plot 
    """    
    
    won, lost, _ = won_lost_for_num_players()

    fig, ax = plt.subplots(figsize=(20,20))


    width = 0.35
    labels = ['0','1','2+']
    x = np.arange(len(labels))
    won_ax = ax.bar(x=x - width/2, height= won['num_players_before'].value_counts(), width=width, label='Won/Broke Even')
    lost_ax = ax.bar(x=x + width/2, height= lost['num_players_before'].value_counts(), width=width, label='Lost')
    ax.legend()
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    ax.set_ylabel('Number of Hands')
    ax.set_xlabel('Number of Players')
    ax.set_title('Number of Hands Won or Lost \n by Number of Players to Enter Pot')

    return ax 

if __name__=="__main__":
    # ax1 = plot_num_players_under3()
    # ax2 = plot_num_players_over3()
    won, lost, _ = won_lost_for_num_players()
    print(won['num_players_before'].value_counts())
    print(won['num_players_before'].value_counts())
    ax3 = plot_together()
    plt.show()