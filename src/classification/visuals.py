import seaborn as sns 
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
plt.style.use('ggplot')


def load_whole():
    '''
    change this to entire dataframe eventually 
    '''
    df = pd.read_csv('/home/sam/Documents/DSI/capstone/poker/data/train_classification_tournaments.csv')
    df = df.drop(df.columns[0], axis = 1)
    won_mask = df['made_or_lost'] == 1
    won = df[won_mask]
    lost_mask = df['made_or_lost'] == 0
    lost = df[lost_mask]
    return won, lost, df

def plot_card_rank(): # probably could use some cleanup 
    _, _,df = load_whole()
    fig, ax = plt.subplots()
    ax = sns.kdeplot(data=df, x='card_rank', hue='made_or_lost', fill=True)
    ax.legend(['won', 'lost'])
    return ax 

def plot_bb():
    _, _,df = load_whole()
    fig, ax = plt.subplots()
    ax = sns.kdeplot(data=df, x='BB_in_stack', hue='made_or_lost', fill=True)
    ax.set(xlim=(0,100))
    ax.legend(['won','lost'])
    return ax 

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

def plot_made_v_lost():
    won, lost, df = load_whole()
    won_percent = round(100 * len(won) / len(df),1)
    lost_percent = round(100 * len(lost) / len(df),1)

    labels = ['Won', 'Lost']
    x = np.arange(len(labels))
    width=.35
    fig, ax = plt.subplots()
    won_ax = ax.bar(x=0 + width/1.5, height=len(won), width=width, color='r', label='won')
    lost_ax = ax.bar(x=1 - width/1.5, height=len(lost), width=width, color='blue', label='lost')

    ax.set_xticks([0 + width/1.5, 1 - width/1.5])
    ax.set_xticklabels(labels)

    plt.text(x=0 + .16, y = 500, s=f'{won_percent}%', fontsize=20)
    plt.text(x=1 - .3, y = 500, s=f'{lost_percent}%', fontsize=20)

    return ax 

if __name__=="__main__":
    
    ax = plot_made_v_lost()
    ax1 = plot_raises()
    plt.show()
