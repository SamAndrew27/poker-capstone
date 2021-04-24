import seaborn as sns 
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
from load_df import load_whole
plt.style.use('ggplot')

plt.rcParams.update({'font.size': 20})

def plot_made_v_lost():
    won, lost, df = load_whole()
    won_percent = round(100 * len(won) / len(df),1)
    lost_percent = round(100 * len(lost) / len(df),1)

    labels = ['Won/Broke Even', 'Lost']
    x = np.arange(len(labels))
    width=.35
    fig, ax = plt.subplots(figsize=(10,10))
    won_ax = ax.bar(x=0 + width/1.5, height=len(won), width=width,  label='Won/Broke Even')
    lost_ax = ax.bar(x=1 - width/1.5, height=len(lost), width=width,  label='Lost')

    ax.set_xticks([0 + width/1.5, 1 - width/1.5])
    ax.set_xticklabels(labels)

    plt.text(x=0 + .16, y = 500, s=f'{won_percent}%', fontsize=25)
    plt.text(x=1 - .3, y = 500, s=f'{lost_percent}%', fontsize=25)
    ax.set_title('Number of Hands \n Won or Lost')
    ax.set_ylabel('Number of Hands')
    # ax.legend()

    fig.tight_layout()

    return ax 

if __name__ == "__main__":
    ax = plot_made_v_lost()
    plt.show()