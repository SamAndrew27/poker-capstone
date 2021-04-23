import seaborn as sns 
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
from load_df import load_whole
plt.style.use('ggplot')

_, _, df= load_whole()
# tabling this stuff, maybe return once you have the other plots in your slides




if __name__=='__main__':
    mask = df['card_rank'] == 20
    aces = df[mask]
    won_mask = aces['made_or_lost'] == 1
    won_aces = aces[won_mask]
    lost_mask = aces['made_or_lost'] == 0
    lost_aces = aces[lost_mask]

    fig, ax = plt.subplots()
    width = .35
    labels = ['Won', 'Lost']
    x = np.arange(len(labels))
    ax.bar(x=x, height=len(won_aces), width=width, label='Won')
    # ax.bar(x=x-.5, height=len(lost_aces), width=width, label= 'Lost')


    # won_ax = ax.bar(x=x - width/2, height= won['raises&reraises'].value_counts(), width=width, label='won')
    # ace_counts = just_aces.value_counts('made_or_lost')
    # ace_counts.index = ['Won', 'Lost']
    # ax.bar(aces['made_or_lost'])
    plt.show()
