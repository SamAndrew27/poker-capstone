import numpy as np 
import pandas as pd

def fill_dependent_columns(df, fill_BB_nans = True, prior_actions=True):
    """creates columns that are created using columns that I previously created

    Args:
        df (DataFrame): DataFrame from SQL Data with columns added in 'columns_from_hand_history' 
        fill_BB_nans (bool, optional): If true will attempt to add values to nans in 'BB'. Defaults to True.
        prior_actions (bool, optional): If True will implement 'prior_actions' and all related columns0. In its current form this will delete Cash game hands Defaults to True.

    Returns:
        DataFrame: DataFrame with additional columns added
    """    

    df['blinds'] = df.apply(lambda row: blinds(row), axis =1)
 
    df['made_money'] = df['won'] > df['bet']
  
    df['made_money'] = df['made_money'].apply(lambda mm: fix_made_money(mm))
  
    df['card_rank'] = df['my_cards'].apply(lambda cards: card_rank(cards))
  
    df['BB'] = df['blinds'].apply(lambda x: BB(x))


    if fill_BB_nans:
        df = fix_BB_nans(df) # consider removing? # way I did this causes a warning 
    
  
    df['BB_in_stack'] = df.apply(lambda row: BB_in_stack(row), axis = 1)
   
    df['net_outcome'] = df['won'] - df['bet']     
   
    df['all_in'] = df.apply(lambda row: all_in(row), axis = 1)
    
    df['money_beyond_blind'] = df.apply(lambda row: money_beyond_blind(row), axis = 1) # whether i put in money in addition to OG blind
  
    df['outcome_relative_to_start'] = (df['starting_stack'] + df['net_outcome']) / df['starting_stack']  # amount I started with +/- how much I won or lost divided by starting stack

    df['made_or_lost'] = df['outcome_relative_to_start'].apply(lambda outcome: made_or_lost(outcome))

    df['num_players_before'] = df['players_acting_before_me'].apply(lambda players: len(players)) # players before me currently in the pot

    df['num_players_after'] = df['players_acting_after_me'].apply(lambda players: len(players)) # players after me currently in the pot

    df['amount_to_call'] = df.apply(lambda row: amount_to_call(row), axis=1)

    df['limps&calls'] = df['limpers'] + df['callers']

    if prior_actions: 

        df = prior_actions_for_stats(df)

        df['prior_actions'] = df['prior_actions'].apply(lambda prior_actions: unlist(prior_actions)) # fix the weird thing I did to create prior actions (take dictionary out of list)

        df['vpip_all_players'] = df['prior_actions'].apply(lambda prior_actions: make_vpip(prior_actions))

        df['vpip_players_after'] = df.apply(lambda row: vpip_players_after(row), axis=1)

        df['vpip_players_before'] = df.apply(lambda row: vpip_players_before(row), axis=1)

        df['num_actions_before_players'] = df.apply(lambda row: actions_witnessed_before(row), axis=1) # number of actions VPIP is created upon

        df['num_actions_after_players'] = df.apply(lambda row: actions_witnessed_after(row), axis=1)  # number of actions VPIP is created upon 

        df['average_table_vpip'] = df['vpip_all_players'].apply(lambda vpip_all_players: average_table_vpip(vpip_all_players)) # does not include me 

        df['total_actions_witnessed'] = df['prior_actions'].apply(lambda prior_actions: total_actions_witnessed(prior_actions))

        df['vpip_relavant_players'] = df.apply(lambda row: vpip_relavant_players(row), axis=1)

        df['total_actions_witnessed_relevant_players'] = df.apply(lambda row: total_actions_witnessed_relevant_players(row), axis=1)

        df['weighted_relevant_vpip'] = df.apply(lambda row: weighted_relevant_vpip(row), axis=1)




    return df 




def blinds(row): # hand history & gametype 
    """Finds blinds from hand - uses presets for cash hands 

    Args:
        row from dataframe, looks at HandHistory/cash_or_tourn

    Returns:
        list: blinds from hand
    """    
    gt = row['cash_or_tourn']
    hh = row['HandHistory']
    if gt == 'Holdem NL':
        blind_list = []
        result = []
        for elem in hh:
            if '[cards]' in elem:
                blind_list.append(elem)
        for elem in blind_list:
            temp = elem.split(' ')
            for s in temp:
                if 'sum' in s:
                    temp2 = s.replace('sum="', '')
                    temp2 = temp2.replace('"', '')
                    result.append(float(temp2))
    else:
        if gt == 'Holdem NL $0.02/$0.05':
            result = [.02, .05]
        if gt == 'Holdem NL $0.20/$0.40':
            result = [.2, .4]
        if gt == 'Holdem NL $0.10/$0.20':
            result = [.1,.2]
    return result 


def fix_made_money(mm):
    """turns made_money from bool into 1/0 bool

    Args:
        mm: made_money column 

    Returns:
        int: 1 = situations where I made money, 0 = situations where I lost money
    """    

    result = 0
    if mm == True:
        result = 1
    else:
        result = 0
    return result


def card_rank(cards):
    """using Bill Chen's formula I am assigning a numeric value to my hole cards

    Args:
        cards (list): my cards, 'my_cards' column 

    Returns:
        int: card's rank 
    """    
    result = 0
    if isinstance(cards, list):
        if len(cards[0]) == 2 and len(cards[1]) == 2:
            c1 = cards[0]
            c2 = cards[1]
            c1_rank = c1[1]
            c2_rank = c2[1]
            c1_suit = c1[0]
            c2_suit = c2[0]
            c_rank = [c1_rank, c2_rank]
            
            
            numeric_card_lst = []
            
            for card in c_rank: # assigning numeric value of card ranks
                if card in ['A', 'K', 'Q', 'J', '1']:
                    numeric_dic = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, '1': 10}
                    numeric_card_lst.append(numeric_dic[card])
                else:
                    numeric_card_lst.append(int(card))
            
            highest = max(numeric_card_lst) # assigning points for highest card
            
            if highest > 10: # points for over 10
                high_vals = {14:10, 13:8, 12:7, 11:6}
                result += high_vals[highest]
            else: # points for 10 & under
                result += highest / 2
                
            
            if c1_suit == c2_suit: # assigning points for whether cards are suited
                result += 2
            
            
            
            val = highest - min(numeric_card_lst) # getting the distance betweeen the cards
            
            if val == 0: # doubling points of pocket pairs 
                result *= 2
                if result < 5: # worth minimum of 5 points
                    result = 5
            else: # now assigning points for connectedness between 
                if val <= 3: # 2 gapper and less
                    result -= val - 1
                else:
                    if val == 4: # 3 gapper
                        result -= val
                    else: # 4 gapper and more
                        result -= 5
            if val <= 2 and val != 0 and numeric_card_lst[0] < 12 and numeric_card_lst[1] < 12:
                result += 1
                
                    
    return result # I elected not to round up as the formula dictates, not sure what benefit it would have in this scenario
 

def BB(x): 
    """Tries to find what BB was

    Args:
        blinds: list of blinds, 'blinds' column

    Returns:
        float: BB, if one was able to be found
    """    
    result = None 
    blinds = x.copy()
    if len(blinds) == 2:
        if max(blinds) / min(blinds) == 2 or max(blinds) < 0.5:
            result = max(x)


    else:
        if len(blinds) > 2:
            BB = blinds.pop(blinds.index(max(blinds)))
            SB = blinds.pop(blinds.index(max(blinds)))
            anti = blinds.pop(blinds.index(max(blinds)))
            if BB / SB == 2 and BB / anti == 10: # maybe just don't include anti element? 
                result = max(x)



    return result 


def BB_in_stack(row):
    """divides stack by the Big Blind

    Args:
        row : used to get starting_stack / BB

    Returns:
        float: number of BB in my stack
    """    
    stack = row['starting_stack']
    BB = row['BB']
    result = None
    if pd.isna(BB) == False and pd.isna(stack) == False:
        result = stack / BB
    
    return result


def all_in(row):
    """Finds whether I went all in or not

    Args:
        row: used to get starting stack/amount I bet

    Returns:
        int: 1 for all in, 0 for not all in 
    """    
    stack = row['starting_stack']
    bet = row['bet']
    result = None
    if stack == bet:
        result = int(1)
    else:
        if stack > 0:
            result = int(0)

    return result


def money_beyond_blind(row):
    """Finds whether I put in money beyond what I blinded

    Args:
        row: row used to get bet and my_blind_anti_total

    Returns:
        int: 1 if I put in money beyond blind, 0 if I did not
    """    
    my_blind = row['my_blind_anti_total']
    my_bet = row['bet']
    result = 0
 
    if my_bet > my_blind:
        result = 1
    return result

# this is currently excluding cash game nulls, probably could just divide by .05, although it's not really important for cash games
def fix_BB_nans(input_df):
    """attempts to fill BB columns that have nulls

    Args:
        input_df (DataFrame): Dataframe we are checking for nulls

    Returns:
        DataFrame: with nulls filled if possible 
    """    
    df = input_df.copy()
    for idx, row in df.iterrows():
        if pd.isnull(row['BB']):
            tourn_num = row['TournamentNumber']
            if pd.isnull(df['BB'].iloc[idx+1]) == False:
                option_1 = df['TournamentNumber'].iloc[idx+1]
                if option_1 == tourn_num:
                    df['BB'].iloc[idx] = df['BB'].iloc[idx+1]
            else:
                if pd.isnull(df['BB'].iloc[idx+2]) == False:
                    option_2 = df['TournamentNumber'].iloc[idx+2]
                    if option_2 == tourn_num:
                        df['BB'].iloc[idx] = df['BB'].iloc[idx+2]                

                         
    return df

# looks at whether outcome relative to start is <1 or is >=1 
# negative class is losing $
# positive class is making $
# this may be redundant, but rather than checking the validity of those columns made a while ago lets do this
def made_or_lost(outcome):
    """Finds whether I made or lost money

    Args:
        outcome_relative_to_start: column which says how much I won or lost relative to starting stack (float)

    Returns:
        int: 1 for made money/broke even, 0 for cases where I lost money
    """    
    if outcome >= 1:
        return 1
    else:
        return 0 


def prior_actions_for_stats(df): # right now we are deleting the cash game hands - I suppose that's not a problem but consider changing it 
    """For each hand creates list of actions players made previously. INADVERTEDLY DELETES CASH HANDS HERE

    Args:
        df : DataFrame

    Returns:
        DataFrame: Dataframe, containing column w/ all the past actions of the players in the hand. 
    """    
    '''
    finds actions of player prior to the hand currently being played 
    '''
    mask = df['TournamentNumber'] != '' # ignores cash hands for time being, make this optional w/ argument (or just make sure non_tournaments not considered in first iteration)? 
    df = df[mask]
    df['prior_actions'] = df.HandHistory.apply(lambda prior_actions: make_lst(prior_actions)) # creates column of empty lists
    unique_TN = df['TournamentNumber'].unique()
    for num in unique_TN: # iterates through all unique tournament numbers 
        mask = df['TournamentNumber'] == num
        tourn_df = df[mask] # create mask with tournament
        for idx, row in tourn_df.iterrows(): # iterates through each row of tournament 
            row_dic = {}
            mask = tourn_df.index < idx
            df_prior = tourn_df[mask] # mask to get hands that occured previously in this tournament 
            for player in row['player_names']: # looping through all players present in hand
                player_actions = []
                for dic in df_prior['action_type']: # looking at all prior hands 
                    if player in dic:
                        player_actions.append(dic[player]) 
                row_dic[player] = player_actions # adds to row dic: key as player name, value as list of prior actions
            df.loc[idx, 'prior_actions'].append(row_dic) # adds row_dic to the empty list in 'prior_actions' for specific row 

    return df


def make_lst(prior_actions): # definitely a better way to do this but this is easy 
    """makes 'prior_actions' in above function, column filled with empty lists

    Args:
        prior_actions ([type]): [description]

    Returns:
        List: empty list filled in above function 
    """    
    return []

def unlist(prior_actions):
    """removes exterior list, leaving just a dictionary in 'prior_actions'

    Args:
        prior_actions (list): list with dictionary in it

    Returns:
        dictionary: dict contained within 'prior_actions'
    """    
    return prior_actions[0]

def make_vpip(prior_actions):
    """finds vpip for all players using prior stats and returns it

    Args:
        prior_actions: dictionary containing prior actions of all players

    Returns:
        dictionary: contains actions of all prior actions for every player in hand
    """    
    result = {}
    if prior_actions != {}:
        for player, actions in prior_actions.items(): # iterate through player dictionaries
            count = 0
            if len(actions) != 0:
                for action in actions: # iterate through actions
                    if action != 0 and action != 4:
                        count += 1
                result[player] = count / len(actions)
            else:
                result[player] = 'No Hands' 
    return result 
                
def vpip_players_after(row):
    """gets vpip of all players yet to make their first action

    Args:
        row: row of dataframe, used to get 'vpip_all_players'/'players_acting_after_me'

    Returns:
        float: average VPIP for all subsuquent players
    """    

    vpips = []
    vpip_dic = row['vpip_all_players'] # dictonary of vpips of each player
    players_after = row['players_acting_after_me']

    if players_after != {}: # skips if there are no players after
        for player in players_after: # look at all players after & find their vpip
            if vpip_dic[player] == 'No Hands':
                continue
            else:
                vpips.append(vpip_dic[player])
    if len(vpips) != 0:
        return np.mean(vpips)

def vpip_players_before(row):
    """gets vpip of all players yet to make their first action

    Args:
        row: row of dataframe, used to get 'vpip_all_players'/'players_acting_before_me'

    Returns:
        float: average VPIP for all players that already entered hand 
    """    
    vpips = []
    vpip_dic = row['vpip_all_players'] # dictonary of vpips of each player
    players_before = row['players_acting_before_me'] # list of players acting before

    if players_before != {}: # skips if there are no players after
        for player in players_before: # look at all players after & find their vpip
            if vpip_dic[player] == 'No Hands':
                continue
            else:
                vpips.append(vpip_dic[player])
    if len(vpips) != 0:
        return np.mean(vpips)

def actions_witnessed_before(row):
    """counts number of actions used to created VPIP of players before

    Args:
        row: row of dataframe, used to get 'prior_actions'/'players_acting_before_me'

    Returns:
        int: number of actions used to create before players vpip stats
    """    
    prior_actions = row['prior_actions']
    total = 0
    for player in row['players_acting_before_me']:
        total += len(prior_actions[player])
    return total 

def actions_witnessed_after(row):
    """counts number of actions used to created VPIP of players after

    Args:
        row: row of dataframe, used to get 'prior_actions'/'players_acting_after_me'

    Returns:
        int: number of actions used to create after players vpip stats
    """    
    prior_actions = row['prior_actions']
    total = 0
    for player in row['players_acting_after_me']:
        total += len(prior_actions[player])
    return total  





def amount_to_call(row):
    """finds how much it would cost me to stay in the hand (call)

    Args:
        row: row of dataframe, used to get 'HandHistory'/'players_names'

    Returns:
        float: bet size I am facing to stay in the hand
    """    
    player_bets = {}
    handhistory = row['HandHistory']
    bb = row['BB']
    bet = 0
    player_name = 0
    for name in row['player_names']: # setting up dictionary with keys of all player names
        player_bets[name] = 0
        
    for elem in handhistory: # getting amount put in prior to betting
        if '[cards]' in elem and ('type="1"' in elem or 'type="2"' in elem): # ignores antis  
            for sub_string in elem.split():
                if 'player' in sub_string:
                    player_name = sub_string.replace('player="', '').replace('"', '') 
                if 'sum' in sub_string:
                    bet = float(sub_string.replace('sum="', '').replace('"', '')) 
                    player_bets[player_name] += bet
            
    

    for idx, elem in enumerate(handhistory): 
        if 'Pocket' in elem:
            start = idx
    subset = handhistory[start+1:] # subset containing preflop action until end
    for idx, elem in enumerate(subset):
        if '</round>' in elem:
            stop = idx
            break 
    subset = subset[:stop] # subset containing just preflop action 
    
    for elem in subset: # iterating through preflop action
        if 'Hero' in elem: # ends iteration if action arrives at me
            break 
        if 'sum="0"' not in elem: # finds cases where bet was made 
            for sub_string in elem.split():
                if 'player' in sub_string:
                    player_name = sub_string.replace('player="', '').replace('"', '') 
                if 'sum' in sub_string:
                    bet = float(sub_string.replace('sum="', '').replace('"', '')) 
                    player_bets[player_name] += bet

    
    if max(player_bets.values()) < bb: # finds if BB was greater than amount bet 
        result = bb # if so sets result = to BB, useful in cases where actual BB was smaller than the actual bet (shortstacks)
    else:
        result = max(player_bets.values())
    result = result - player_bets.get('Hero', 0) # subtracts in case I am small blind or BB
    result = result / bb # puts result in BB format
    
    return result 


def average_table_vpip(vpip_all_players):
    """calculates the average VPIP of the table

    Args:
        vpip_all_players (dictionary): vpip of all players at table

    Returns:
        float: average VPIP of players at the table   
    """    


    vpip_lst = []
    for key, val in vpip_all_players.items():
        if key == 'Hero' or val == 'No Hands':
            continue
        else:
            vpip_lst.append(val)
    return np.mean(vpip_lst)


def total_actions_witnessed(prior_actions):
    """number of actions used to caclulate table VPIP

    Args:
        prior_actions: dictionary containing prior actions of all players

    Returns:
        int: count of actions used to calculate average table vpip
    """    
    total = 0
    for player, actions in prior_actions.items():
        if player != 'Hero':
            total += len(actions)
    return total 



def vpip_relavant_players(row):
    """vpip of all players who have entered the hand or are yet to act

    Args:
        row: row of dataframe, used to get 'players_acting_before_me'/'players_acting_after_me'/'vpip_all_players'

    Returns:
        float: average vpip of relevant players (those in hand/those yet to act)
    """    
    vpip_lst = []
    players_before = row['players_acting_before_me']
    players_after = row['players_acting_after_me']
    vpip_dic = row['vpip_all_players']
    for player in players_before:
        if vpip_dic[player] != 'No Hands':
            vpip_lst.append(vpip_dic[player])
    for player in players_after:
        if vpip_dic[player] != 'No Hands':
            vpip_lst.append(vpip_dic[player])
        
    return np.mean(vpip_lst)

def total_actions_witnessed_relevant_players(row):
    """"number of actions used to calculate relevant player stats

    Args:
        row: row of dataframe, used to get 'players_acting_before_me'/'players_acting_after_me'/'prior_actions'

    Returns:
        int: total number of relevant player actions
    """    
    players_before = row['players_acting_before_me']
    players_after = row['players_acting_after_me']
    prior_actions = row['prior_actions']
    total = 0
    for player in players_before:
        total += len(prior_actions[player])
    for player in players_after:
        total += len(prior_actions[player])  
    return total 

def weighted_relevant_vpip(row):
    """VPIP with scores weighted according to how many actions were used to calculate them 
    (same as relevant player stuff but w/ weighting)

    Args:
        row: row of dataframe, used to get 'players_acting_before_me'/'players_acting_after_me'/'vpip_all_players'

    Returns:
        float: average vpips of relevant players, weighted according to # of actions used in their creation
    """    

    vpip_lst = []
    players_before = row['players_acting_before_me']
    players_after = row['players_acting_after_me']
    prior_actions = row['prior_actions']
    vpip_dic = row['vpip_all_players']
    for player in players_before:
        if vpip_dic[player] != 'No Hands':
            num_actions = len(prior_actions[player])
            for num in range(num_actions):
                vpip_lst.append(vpip_dic[player])
    for player in players_after:
        if vpip_dic[player] != 'No Hands':
            num_actions = len(prior_actions[player])
            for num in range(num_actions):
                vpip_lst.append(vpip_dic[player])
        
    return np.mean(vpip_lst)
    

if __name__=="__main__":
    pass 
