import pandas as pd

def fill_dependent_columns(df, fill_BB_nans = False):

    df['blinds'] = df.apply(lambda x: blinds(x), axis =1)
 
    df['made_money'] = df['won'] > df['bet']
  
    df['made_money'] = df['made_money'].apply(lambda x: fix_made_money(x))
  
    df['card_rank'] = df['my_cards'].apply(lambda x: cards_numeric(x))
  
    df['BB'] = df['blinds'].apply(lambda x: BB(x))


    if fill_BB_nans == True:
        df = fix_BB_nans(df) # consider removing? # way I did this causes a warning 
    
  
    df['BB_in_stack'] = df.apply(lambda x: BB_in_stack(x['starting_stack'], x['BB']), axis = 1)
   
    df['net_outcome'] = df['won'] - df['bet']     
   
    df['all_in'] = df.apply(lambda x: all_in(x['starting_stack'], x['bet']), axis = 1)
    
    df['money_beyond_blind'] = df.apply(lambda x: money_beyond_blind(x), axis = 1) # whether i put in money in addition to OG blind
  
    df['outcome_relative_to_start'] = (df['starting_stack'] + df['net_outcome']) / df['starting_stack']  

    df['made_or_lost'] = df['outcome_relative_to_start'].apply(lambda x: made_or_lost(x))

    df = prior_actions_for_stats(df)

    return df 




def blinds(x): # hand history & gametype 
    gt = x['cash_or_tourn']
    hh = x['HandHistory']
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


def fix_made_money(x):
    result = 0
    if x == True:
        result = 1
    else:
        result = 0
    return result


def cards_numeric(x):
    result = 0
    if isinstance(x, list):
        if len(x[0]) == 2 and len(x[1]) == 2:
            c1 = x[0]
            c2 = x[1]
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


def BB_in_stack(stack, BB):
    result = None
    if pd.isna(BB) == False and pd.isna(stack) == False:
        result = stack / BB
    
    return result


def all_in(stack, bet):
    result = None
    if stack == bet:
        result = int(1)
    else:
        if stack > 0:
            result = int(0)

    return result


def money_beyond_blind(x):
    my_blind = x['my_blind_anti_total']
    my_bet = x['bet']
    result = 0
 
    if my_bet > my_blind:
        result = 1
    return result

# this is currently excluding cash game nulls, probably could just divide by .05, although it's not really important for cash games
def fix_BB_nans(input_df):
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
def made_or_lost(x):
    if x >= 1:
        return 1
    else:
        return 0 


def prior_actions_for_stats(df):
    '''
    finds actions of player prior to the hand currently being played 
    '''
    mask = df['TournamentNumber'] != '' # ignores cash hands for time being, make this optional w/ argument? 
    df = df[mask]
    df['prior_actions'] = df.HandHistory.apply(lambda x: make_lst(x))
    unique_TN = df['TournamentNumber'].unique()
    for num in unique_TN: # iterates through all unique tournament numbers
        mask = df['TournamentNumber'] == num
        tourn_df = df[mask]
        for idx, row in tourn_df.iterrows(): # go through each row of tournament 
            row_dic = {}
            mask = tourn_df.index < idx
            df_prior = tourn_df[mask] # hands that occured previously in this tournament 
            for player in row['player_names']: # looping through all players present in hand
                player_actions = []
                for dic in df_prior['action_type']: # looking at all prior hands 
                    if player in dic:
                        player_actions.append(dic[player])
                row_dic[player] = player_actions
            df.loc[idx, 'prior_actions'].append(row_dic)

    return df


def make_lst(x): # definitely a better way to do this but this is easy 
    return []
