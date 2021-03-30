import pandas as pd 



def fill_betting_columns(df):
    df['flop_bet'] = df.apply(lambda x: flop_bet(x), axis = 1)

    df['turn_bet'] = df.apply(lambda x: turn_bet(x), axis = 1)

    df['river_bet'] = df.apply(lambda x: river_bet(x), axis = 1)

    df['preflop_bet'] = df['bet'] - (df['flop_bet'] + df['turn_bet'] + df['river_bet'] + df['my_blind_anti_total'])

    df['high_card'] = df['my_cards'].apply(lambda x: high_card(x))

    df['low_card'] = df['my_cards'].apply(lambda x: low_card(x)) # redundant with gap/high card? 

    df['suited'] = df['my_cards'].apply(lambda x: suited(x))

    df['pocket_pair'] = df['my_cards'].apply(lambda x: pocket_pair(x)) # redundant with the gap column?

    df['gap'] = df['my_cards'].apply(lambda x: gap(x))

    return df


##############################################
def flop_bet(x): # takes in HandHistory and money_beyond_blind
    hh = x['HandHistory']
    mbb = x['money_beyond_blind']
    result = 0
    subset = []
    action_lst = []
    if mbb == 1: # skips process if no money put in beyond blind
        start = 0
        stop = 0
        for idx, s in enumerate(hh): # gets range to look for hero flop bet in 
            if 'Flop' in s:
                start = idx + 1
            if 'round no="3' in s:
                stop = idx
                break 
        if start != 0:
            if stop == 0: # in case there was no betting after flop 
                stop = -1 
            subset = hh[start:stop]
        if subset != []: # continues if we have a subset to work with 
            for s in subset:
                if 'player="Hero"' in s:
                    for sub_string in s.split():
                        action_lst.append(sub_string)
        if action_lst != []:
            for s in action_lst:
                if 'sum=' in s:
                    result = float(s.replace('sum="', '').replace('"', '').strip())
    
    return result 
                   

def turn_bet(x): # takes in HandHistory and money_beyond_blind
    hh = x['HandHistory']
    mbb = x['money_beyond_blind']
    result = 0
    subset = []
    action_lst = [] # list of actions I made in the round of betting
    start = 0
    stop = 0
    if mbb == 1: # skips process if no money put in beyond blind

        for idx, s in enumerate(hh): # gets range to look for hero flop bet in 
            if 'Turn' in s:
                start = idx + 1
            if 'round no="4' in s:
                stop = idx
                break 
        if start != 0:
            if stop == 0: # in case there was no betting after flop 
                stop = -1 
            subset = hh[start:stop]
        if subset != []: # continues if we have a subset to work with, maybe remove this line 
            for s in subset:
                if 'player="Hero"' in s:
                    for sub_string in s.split():
                        action_lst.append(sub_string)
        if action_lst != []:
            for s in action_lst:
                if 'sum=' in s:
                    result += float(s.replace('sum="', '').replace('"', '').strip())
    
    return result


def river_bet(x): # takes in HandHistory and money_beyond_blind
    hh = x['HandHistory']
    mbb = x['money_beyond_blind']
    result = 0
    subset = []
    action_lst = []
    if mbb == 1: # skips process if no money put in beyond blind
        start = 0
        for idx, s in enumerate(hh): # gets range to look for hero flop bet in 
            if 'River' in s:
                start = idx + 1
                break 
        if start != 0:
            subset = hh[start:]
        if subset != []: # continues if we have a subset to work with 
            for s in subset:
                if 'player="Hero"' in s:
                    for sub_string in s.split():
                        action_lst.append(sub_string)
        if action_lst != []:
            for s in action_lst:
                if 'sum=' in s:
                    result = float(s.replace('sum="', '').replace('"', '').strip())
    
    return result 

def high_card(x):
    result = None
    if isinstance(x, list):
        if len(x[0]) == 2 and len(x[1]) == 2:
            c1 = x[0]
            c2 = x[1]
            c1_rank = c1[1]
            c2_rank = c2[1]
            numeric_card_lst = []
            c_rank = [c1_rank, c2_rank]
            for card in c_rank: # assigning numeric value of card ranks
                if card in ['A', 'K', 'Q', 'J', '1']:
                    numeric_dic = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, '1': 10}
                    numeric_card_lst.append(numeric_dic[card])
                else:
                    numeric_card_lst.append(int(card))
            result = int(max(numeric_card_lst))
    return result

def low_card(x):
    result = None
    if isinstance(x, list):
        if len(x[0]) == 2 and len(x[1]) == 2:
            c1 = x[0]
            c2 = x[1]
            c1_rank = c1[1]
            c2_rank = c2[1]
            numeric_card_lst = []
            c_rank = [c1_rank, c2_rank]
            for card in c_rank: # assigning numeric value of card ranks
                if card in ['A', 'K', 'Q', 'J', '1']:
                    numeric_dic = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, '1': 10}
                    numeric_card_lst.append(numeric_dic[card])
                else:
                    numeric_card_lst.append(int(card))
            result = int(min(numeric_card_lst))
    return result  

def suited(x):
    result = 0
    if isinstance(x, list):
        if len(x[0]) == 2 and len(x[1]) == 2:
            c1 = x[0]
            c2 = x[1]
            c1_suit = c1[0]
            c2_suit = c2[0]
            if c2_suit == c1_suit:
                result = 1
    return result 

def pocket_pair(x):
    result = 0
    if isinstance(x, list):
        if len(x[0]) == 2 and len(x[1]) == 2:
            c1 = x[0]
            c2 = x[1]
            c1_rank = c1[1]
            c2_rank = c2[1]
            if c1_rank == c2_rank:
                result = 1
    return result 


def gap(x):
    result = None
    if isinstance(x, list):
        if len(x[0]) == 2 and len(x[1]) == 2:
            c1 = x[0]
            c2 = x[1]
            c1_rank = c1[1]
            c2_rank = c2[1]  
            c_rank = [c1_rank, c2_rank]                        
            numeric_card_lst = []
            
            for card in c_rank: # assigning numeric value of card ranks
                if card in ['A', 'K', 'Q', 'J', '1']:
                    numeric_dic = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, '1': 10}
                    numeric_card_lst.append(numeric_dic[card])
                else:
                    numeric_card_lst.append(int(card))
                    
            result = max(numeric_card_lst) - min(numeric_card_lst)
    return result 