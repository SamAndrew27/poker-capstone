import pandas as pd
import matplotlib.pyplot as plt
from data_prep import get_cash, get_tournaments, put_in_money




def training_and_holdout_together():
    df = pd.read_csv('/home/sam/Documents/DSI/capstone/poker/data/df_for_classification.csv')
    df = get_tournaments(df)
    df = put_in_money(df)
    df = df.dropna(subset = ['outcome_relative_to_start','buyin', 
                            'BB_in_stack', 'total_players', 'position',  
                            'low_card', 'high_card', 'suited', 'pocket_pair', 'card_rank' ])
    df = df[['buyin', 'BB_in_stack', 'total_players', 
             'position', 'low_card', 'high_card', 
             'suited', 'pocket_pair', 'card_rank', 
             'hour', 'days_since_start', 'hand_frequency', 'made_or_lost']]
    return df


def aces_plot():
    df = training_and_holdout_together()
    mask = df.card_rank ==20
    just_aces = df[mask]
    plt.rcParams.update({'font.size': 18})

    ace_counts = just_aces.value_counts('made_or_lost')
    ace_counts.index = ['Won', 'Lost']


    ace_counts.plot.bar()
    plt.title('Hand Outcome with Pocket Aces')
    plt.ylabel('Number of Hands')
    plt.xticks(rotation=0)
    plt.show()

def won_lost_plot():
    df = training_and_holdout_together()
    made_or_lost = df.value_counts('made_or_lost')
    made_or_lost.index = ['Won', 'Lost']
    plt.rcParams.update({'font.size': 18})
    made_or_lost.plot.bar()
    plt.title('Won vs Lost For Entire Dataset')
    plt.ylabel('Number of Hands')
    plt.xticks(rotation=0)

    # plt.savefig('total_made_lost.png')
    plt.show()
if __name__ == "__main__":
    won_lost_plot()
