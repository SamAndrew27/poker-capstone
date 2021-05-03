import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd

from load_df import split_won_lost

plt.style.use('ggplot')

_, _, df= split_won_lost()
aces = df[df['card_rank'] == 20]
won_aces = aces[aces['made_or_lost'] == 1]
lost_aces = aces[aces['made_or_lost'] == 0]
fig, ax = plt.subplots()
width = .35
labels = ['Won', 'Lost']
x = np.arange(len(labels))
won_ax = ax.bar(x=x[0], height=len(won_aces))
lost_ax = ax.bar(x=x[1], height=len(lost_aces))
ax.set_xticklabels(labels)
ax.set_xticks(x)
ax.set_ylabel('Number of Hands')
ax.set_title('Number of Hands Won or Lost \n With Aces')


if __name__=='__main__':
    plt.show()





