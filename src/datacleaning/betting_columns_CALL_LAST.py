import pandas as pd 



def fill_betting_columns(df):
    """Takes in dataframe and creates new columns with functions below

    Args:
        df: pandas DataFrame

    Returns:
        pandas dataframe: same as input with additional columns
    """    
    
    df['flop_bet'] = df.apply(lambda row: flop_bet(row), axis = 1)

    df['turn_bet'] = df.apply(lambda row: turn_bet(row), axis = 1)

    df['river_bet'] = df.apply(lambda row: river_bet(row), axis = 1)

    df['preflop_bet'] = df['bet'] - (df['flop_bet'] + df['turn_bet'] + df['river_bet'] + df['my_blind_anti_total'])

    df['high_card'] = df['my_cards'].apply(lambda cards: high_card(cards))

    df['low_card'] = df['my_cards'].apply(lambda cards: low_card(cards)) # redundant with gap/high card? 

    df['suited'] = df['my_cards'].apply(lambda cards: suited(cards))

    df['pocket_pair'] = df.apply(lambda row: pocket_pair(row), axis=1)

    df['gap'] = df['high_card'] - df['low_card']

    return df


##############################################
def flop_bet(row): # takes in HandHistory and money_beyond_blind
    
    """finds value of my flop bet(s) if I made one. In other words finds all the money I put in during the flop 
    Uses 'money_beyond_blind' and 'HandHistory' to determine size of my flop bet.
    
    
    Args:
        row of dataframe, extract HandHistory data and money_beyond_blind data: 

    Returns:
        float: amount I bet 
    """    

    hh = row['HandHistory']
    mbb = row['money_beyond_blind']
    result = 0
    subset = []
    action_lst = [] # list of all of Hero's actions 
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
                   

def turn_bet(row): # takes in HandHistory and money_beyond_blind
    """finds how much $ hero put in on the turn 

    Args:
        row of dataframe, 2 values used, HandHistory & 'money_beyond_blind'

    Returns:
        float: amount bet
    """    

    hh = row['HandHistory']
    mbb = row['money_beyond_blind']
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


def river_bet(row): # takes in HandHistory and money_beyond_blind
    """finds how much $ hero put in on the river

    Args:
        row of dataframe, 2 values used, HandHistory & 'money_beyond_blind'

    Returns:
        float: amount bet
    """    

    hh = row['HandHistory']
    mbb = row['money_beyond_blind']
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

def high_card(cards):
    """finds value of highest card - if cards are equal values will be the same

    Args:
        cards: list of my 2 cards

    Returns:
        int: value of highest card (2 for 2, 14 for Ace)
    """    
    
    result = None
    if isinstance(cards, list):
        if len(cards[0]) == 2 and len(cards[1]) == 2:# checking that I have cards
            c1 = cards[0]
            c2 =cards[1]
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

def low_card(cards):
    """finds value of lowest card - if cards are equal values will be the same 

    Args:
        cards: list of my 2 cards

    Returns:
        int: value of highest card (2 for 2, 14 for Ace)
    """    
    result = None
    if isinstance(cards, list):
        if len(cards[0]) == 2 and len(cards[1]) == 2:# checking that I have cards
            c1 = cards[0]
            c2 = cards[1]
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

def suited(cards):
    """finds whether my 2 cards are suited 

    Args:
        cards: list of my 2 cards

    Returns:
        int: 0 for unsuited, 1 for suited
    """    
    result = 0
    if isinstance(cards, list):
        if len(cards[0]) == 2 and len(cards[1]) == 2:# checking that I have cards
            c1 = cards[0]
            c2 = cards[1]
            c1_suit = c1[0]
            c2_suit = c2[0]
            if c2_suit == c1_suit:
                result = 1
    return result 


def pocket_pair(row):
    """looks at high card and low card to determine if 2 are a pocket pair

    Args:
        row (DataFrame Row): row of DF used for apply function. Uses high_card / low_card

    Returns:
        int: 1 if cards are the same, 0 if they are not 
    """    
    if row['high_card'] == row['low_card']:
        return 1
    else:
        return 0 