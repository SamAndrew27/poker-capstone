import pandas as pd


def fill_HH_columns(df):
    df['buyin'] = df['HandHistory'].apply(lambda row: buyin(row)) 

    df['cash_or_tourn'] = df['HandHistory'].apply(lambda x: gametype(x)) # to discern between cash & tournaments

    df['my_blind_anti_total'] = df['HandHistory'].apply(lambda x: my_blind_anti_total(x)) # how much I put in as default (blind(/anti))

    #df['the_deck'] = df['HandHistory'].apply(lambda row: possible_cards(row)) # retiring this function, could probably be removed entirely 

    df['my_cards'] = df['HandHistory'].apply(lambda row: hole_cards(row)) # my cards 
    
    df['starting_stack'] = df['HandHistory'].apply(lambda row: start_stack(row))
    
    df['tournament_type'] = df['HandHistory'].apply(lambda row: tournament_type(row))

    df['won'] = df['HandHistory'].apply(lambda row: won(row))

    df['bet'] = df['HandHistory'].apply(lambda row: bet(row))

    df['total_players'] = df['HandHistory'].apply(lambda x: total_players(x))

    df['position'] = df['HandHistory'].apply(lambda x: position(x))

    df['table_max_players'] = df['HandHistory'].apply(lambda x: table_max(x))

    # pretty sure this requires edits for edge case, refer to function below
    df['bets_before_my_preflop_action'] = df.HandHistory.apply(lambda x: bets_before_my_preflop_action(x))

    df['action_type'] = df.HandHistory.apply(lambda x: action_type(x))

    df['player_names'] = df['HandHistory'].apply(lambda x: player_names(x)) # for use by other functions 

    df['players_acting_before_me'] = df.HandHistory.apply(lambda x: players_before(x))

    df['players_acting_after_me'] = df.HandHistory.apply(lambda x: players_after(x)) # this might not account for cases where action was folded leading to some players never making an action. If we end up using data for hands where some players did not have to act we will have to develop a more robust function

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
        if 'Pocket' in elem and 'Hero' in elem: # looks for string where my cards are listed
            temp = elem.split(' ') # split and iterate through that string
            for s in temp:
                if 'Hero' in s: # gets card 1 
                    c1 = s.replace('player="Hero">', '')
                    c1 = c1.replace('0', '')
                if '</cards>' in s: # gets card 2
                    c2 = s.replace('</cards>', '')
                    c2 = c2.replace('0', '')
    if c1 != '':
        cards = [c1, c2] # puts cards if list if they exist
        return cards
    else:
        return None


def start_stack(x): 
    '''
    finds amount of chips hero has at start of hand
    '''
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
    '''
    find the type of tournament/game type 
    '''
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
    '''
    amount I won in the hand 
    '''
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
    '''
    total amount that I bet 
    '''
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
    '''
    number of players in the hand 
    '''
    count = 0
    for elem in x:
        if 'Pocket' in elem:
            count += 1
    return count 


def position(x):
    '''
    finds what seat I was sitting in
    1st position (generally small blind) is considered a 1
    last postion (generally dealer seat) = the total number of players at the table
    these values are returned as fractions, so 1/x, in the case of last position x/x 
    '''
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



def bets_before_my_preflop_action(x):
    '''
    finds bets before my bet
    does not include blinds, but should it???
    '''
    start = 0
    stop = 0
    total=0
    subset = []
    for idx, elem in enumerate(x): # find beginning/end of preflop action
        if 'Pocket' in elem:
            start = idx
        if '<round no="2">' in elem: # WILL probably have to change this for instances when there was no round2

            stop = idx
    if stop != 0:
        subset = x[start+1:stop-1] 
        for idx, elem in enumerate(subset): # iterates through subset to find my first action 
            if 'Hero' in elem:
                subset = subset[:idx]
                break 
        for elem in subset:
            for elem in elem.split():
                if 'sum' in elem:
                    total += float(elem.replace('sum="', '').replace('"',''))
    
    return total
        

def action_type(x):
    '''
    finds all action types a player made preflop 
    '''
    result = {}
    start = 0
    stop = 0
    player = None
    action_type = None 
    for idx, elem in enumerate(x): # finds start of preflop action 
        if 'Pocket' in elem:
            start = idx
    subset = x[start+1:]
    for idx, elem in enumerate(subset):# finds end of preflop action
        if '</round>' in elem:
            stop = idx
            break 
    subset = subset[:stop]
    
    for elem in subset: # iterating through preflop action to find player/type 
        for sub_elem in elem.split():
            if 'player' in sub_elem:
                player = sub_elem.replace('player="', '').replace('"', '')
            if 'type' in sub_elem:
                action_type = int(sub_elem.replace('type="', '').replace('"', ''))
        if player in result: # checks to see if player has already taken an action 
            break
        else:
            result[player] = action_type
    return result 



def player_names(x):
    player = None
    result = []
    for elem in x:
        if 'dealer' in elem: 
            for sub_elem in elem.split(): # finds lines where player names are specified 
                if 'name' in sub_elem:
                    player = sub_elem.replace('name="', '').replace('"', '')
                    result.append(player)
                    break 
    return result 


def players_before(x):
    start = 0
    stop = 0
    players_before = [] # list of players before
    for idx, elem in enumerate(x): # list of players after 
        if 'Pocket' in elem:
            start = idx
    subset = x[start+1:] # subset containing preflop action until end
    for idx, elem in enumerate(subset):
        if '</round>' in elem:
            stop = idx
            break 
    subset = subset[:stop] # subset containing just preflop action 
    for elem in subset:
        if 'Hero' in elem: # break if we find hero 
            break
        else:
            for sub_elem in elem.split():
                if 'player' in sub_elem:
                    player_name = sub_elem.replace('player="', '').replace('"', '')
                    players_before.append(player_name)
    return players_before

def players_after(x):
    start = 0
    stop = 0
    hero_found = False
    players_before = set() # set of players before
    players_after = set()
    for idx, elem in enumerate(x): # list of players after 
        if 'Pocket' in elem:
            start = idx
    subset = x[start+1:] # subset containing preflop action until end
    for idx, elem in enumerate(subset):
        if '</round>' in elem:
            stop = idx
            break 
    subset = subset[:stop] # subset containing just preflop action 
    for elem in subset: 
        if 'Hero' in elem: # set to true and skip if hero in elem
            hero_found = True
            continue
        else:
            for sub_elem in elem.split(): 
                if 'player' in sub_elem:
                    player_name = sub_elem.replace('player="', '').replace('"', '') 
                    if hero_found == False: # if hero yet to act add to players before
                        players_before.add(player_name)
                    else:
                        if player_name in players_before: # check to see that player hasn't already acted
                            break
                        else:
                            players_after.add(player_name) # if player hasn't acted add to players after

    return players_after



# almost certainly won't use this, application too difficult for scope of this week 
# def possible_cards(x): # will do this first, and then remove cards in seperate functions, still not sure how to deal with all in vs seeing later action
#     deck = []
#     for s in ['D', 'S', 'C', 'H']:
#         for c in ['2','3','4', '5', '6', '7', '8', '9', '1', 'J', 'Q', 'K', 'A']: # making 10 just 1 for consistency sake
#             temp = s + c
#             deck.append(temp)
#     return deck 