import pandas as pd


def fill_HH_columns(df):
    df['buyin'] = df['HandHistory'].apply(lambda row: buyin(row)) 

    df['cash_or_tourn'] = df['HandHistory'].apply(lambda x: gametype(x)) # to discern between cash & tournaments

    df['my_blind_anti_total'] = df['HandHistory'].apply(lambda x: my_blind_anti_total(x)) # how much I put in as default (blind(/anti))

    #df['the_deck'] = df['HandHistory'].apply(lambda row: possible_cards(row))

    df['my_cards'] = df['HandHistory'].apply(lambda row: hole_cards(row)) # my cards 
    
    df['starting_stack'] = df['HandHistory'].apply(lambda row: start_stack(row))
    
    df['tournament_type'] = df['HandHistory'].apply(lambda row: tournament_type(row))

    df['won'] = df['HandHistory'].apply(lambda row: won(row))

    df['bet'] = df['HandHistory'].apply(lambda row: bet(row))

    df['total_players'] = df['HandHistory'].apply(lambda x: total_players(x))

    df['position'] = df['HandHistory'].apply(lambda x: position(x))

    df['table_max_players'] = df['HandHistory'].apply(lambda x: table_max(x))


    return df



##############################################################################################

# functions that do these processes 

def buyin(x): 
    for elem in x:
        if 'totalbuyin' in elem:
            temp = elem 
            temp = temp.replace('<totalbuyin>$', '')
            temp = temp.replace('</totalbuyin>', '')
            return float(temp)


def gametype(x):
    temp = None
    for elem in x:
        if 'gametype' in elem:
            temp = elem.replace('<gametype>', '').replace('</gametype>', '').strip()
            break
    return temp




def hole_cards(x):
    c1 = ''
    c2 = ''
    for elem in x:
        if 'Pocket' in elem and 'Hero' in elem:
            temp = elem.split(' ')
            for s in temp:
                if 'Hero' in s:
                    c1 = s.replace('player="Hero">', '')
                    c1 = c1.replace('0', '')
                if '</cards>' in s:
                    c2 = s.replace('</cards>', '')
                    c2 = c2.replace('0', '')
    if c1 != '':
        cards = [c1, c2]
        return cards
    else:
        return None


def start_stack(x):
    result = None
    temp = ''
    for elem in x:
        if 'Hero' in elem and 'addon' in elem:
            temp = elem
    
    if temp != '':
        temp = temp.split(' ')
        for elem in temp:
            if 'chips' in elem:
                result = elem.replace('chips="', '')
                result = result.replace('"', '')
                result = float(result)
    return result 

# probably not going to be used, but may be useful so leaving for now
def tournament_type(x):
    result = ''
    cut = 0
    counter = 0
    for elem in x:
        if '<tournamentname>' in elem:
            temp = elem
            cut = temp.count('(') 
            temp = temp.replace('<tournamentname>', '')
            
            for char in temp:
                if char != '(':
                    result += char
                else:
                    counter += 1
                    if counter == cut:
                        break 
                    else:
                        result += char
    result = result.rstrip()
    result = result.replace('amp;', '')
    if 'Table3' in result:
        result = 'Jackpot Sit & Go $0.50'
    return result 

def won(x):
    won = ''
    temp = ''
    result = 0
    for elem in x:
        if 'Hero' in elem and 'addon' in elem:
            temp = elem
    
    if temp != '':
        temp = temp.split(' ')
        for elem in temp:
            if 'win' in elem:
                won = elem.replace('win="', '')
                won = won.replace('"', '')
                result = float(won)
    return result 


def bet(x):
    bet = ''
    temp = ''
    result = None
    for elem in x:
        if 'Hero' in elem and 'addon' in elem:
            temp = elem
    
    if temp != '':
        temp = temp.split(' ')
        for elem in temp:
            if 'bet' in elem:
                bet = elem.replace('bet="', '').replace('"', '')
                result = float(bet)
    return result 

def total_players(x):
    count = 0
    for elem in x:
        if 'Pocket' in elem:
            count += 1
    return count 


def position(x):
    pos_lst = []
    dealer_pos = 0
    dealer_exists = False
    hero_counter = 0
    hero_found = False
    result = None 
    hero_pos = 0
    SB = ''
    for elem in x: # find all initial seatings
        if 'dealer' in elem:
            pos_lst.append(elem)

            
    for idx, elem in enumerate(pos_lst):
        if 'dealer="1"' in elem:
            dealer_pos = idx
            dealer_exists = True
            break
        
    if dealer_exists == False:
        for elem in x:
            if 'type="1"' in elem and '[cards]' in elem:# finds SB
                for sub_string in elem.split(): # iterates through SB to find player name
                    if 'player=' in sub_string:
                        SB = sub_string.replace('player="', '').replace('"','')
                        break
        for idx, elem in enumerate(pos_lst): # iterate through pos_lst to get SB position
            if SB in elem:
                SB_idx = idx
                break
        if SB_idx == 0:
            dealer_pos = len(pos_lst) - 1 # if SB is the 1st in list
        else:
            dealer_pos = SB_idx - 1 # otherwise just backstep 1
            
    if dealer_pos != len(pos_lst) - 1: # if dealer isn't in last position
        beginning = pos_lst[dealer_pos + 1 : ] # subset so lists are sequential
        rest = pos_lst[ : dealer_pos + 1]
        for elem in beginning: # first part of list
            if 'name="Hero"' in elem: # in the case of hero being found
                hero_counter += 1
                hero_pos = hero_counter
                hero_found = True 
                break 
            else:
                hero_counter += 1
        if hero_found == False: # if hero not found in first iteration
            for elem in rest:
                if 'name="Hero"' in elem:
                    hero_counter += 1
                    hero_pos = hero_counter
                    hero_found = True
                    break
                else:
                    hero_counter += 1
    else:
        for elem in pos_lst: # in the event the dealer is in last position
            if 'name="Hero"' in elem:
                hero_counter += 1
                hero_pos = hero_counter
                hero_found = True
                break
            else:
                hero_counter += 1

    if hero_found:
        result = hero_pos / len(pos_lst) # divides position by total number of players
            
    return result

    
def table_max(x):
    result = None
    for elem in x:
        if 'maxplayers' in elem:
            result = int(elem.replace('<maxplayers>', '').replace('</maxplayers>',''))
            break
    return result 



def my_blind_anti_total(x):
    action_list = []
    result = 0
    for elem in x:
        if '[cards]' in elem and 'Hero' in elem:
            action_list.append(elem)
    for elem in action_list:
        for sub_string in elem.split():
            if 'sum' in sub_string:
                result += float(sub_string.replace('sum="', '').replace('"', '').strip())
    return result 









# almost certainly won't use this, application too difficult for scope of this week 
# def possible_cards(x): # will do this first, and then remove cards in seperate functions, still not sure how to deal with all in vs seeing later action
#     deck = []
#     for s in ['D', 'S', 'C', 'H']:
#         for c in ['2','3','4', '5', '6', '7', '8', '9', '1', 'J', 'Q', 'K', 'A']: # making 10 just 1 for consistency sake
#             temp = s + c
#             deck.append(temp)
#     return deck 