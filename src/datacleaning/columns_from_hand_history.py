import pandas as pd


def fill_HH_columns(df):
    """takes in dataframe and uses HandHistory column to create the below features

    Args:
        df (DataFrame): Dataframe created using SQL DriveHud backup

    Returns:
        DataFrame: same as dataframe input with additional columns 
    """    
    df['buyin'] = df['HandHistory'].apply(lambda hh: buyin(hh)) 

    df['cash_or_tourn'] = df['HandHistory'].apply(lambda hh: gametype(hh)) # to discern between cash & tournaments

    df['my_blind_anti_total'] = df['HandHistory'].apply(lambda hh: my_blind_anti_total(hh)) # how much I put in as default (blind(/anti))

    df['my_cards'] = df['HandHistory'].apply(lambda hh: hole_cards(hh)) # my cards 
    
    df['starting_stack'] = df['HandHistory'].apply(lambda hh: start_stack(hh))
    
    df['tournament_type'] = df['HandHistory'].apply(lambda hh: tournament_type(hh))

    df['won'] = df['HandHistory'].apply(lambda hh: won(hh))

    df['bet'] = df['HandHistory'].apply(lambda hh: bet(hh))

    df['total_players'] = df['HandHistory'].apply(lambda hh: total_players(hh))

    df['position'] = df['HandHistory'].apply(lambda hh: position(hh))

    df['table_max_players'] = df['HandHistory'].apply(lambda hh: table_max(hh))

    # pretty sure this requires edits for edge case, refer to function below
    df['bets_before_my_preflop_action'] = df.HandHistory.apply(lambda hh: bets_before_my_preflop_action(hh))

    df['action_type'] = df['HandHistory'].apply(lambda hh: action_type(hh))

    df['player_names'] = df['HandHistory'].apply(lambda hh: player_names(hh)) # for use by other functions 

    df['players_acting_before_me'] = df['HandHistory'].apply(lambda hh: players_before(hh)) # does not include players who folded 

    df['players_acting_after_me'] = df['HandHistory'].apply(lambda hh: players_after(hh)) # this might not account for cases where action was folded leading to some players never making an action. If we end up using data for hands where some players did not have to act we will have to develop a more robust function

    df['limpers'] = df['HandHistory'].apply(lambda hh: limpers(hh))

    df['raises&reraises'] = df['HandHistory'].apply(lambda hh: raises_and_reraises(hh))

    df['callers'] = df['HandHistory'].apply(lambda hh: callers(hh))

    return df



##############################################################################################

# functions that do these processes 

def buyin(hh): 
    """gets buy-in of the tournament, fairly certain cash games still have some sort of value here? 

    Args:
        hh: 'HandHistory' column, string data of hands 

    Returns:
        float: buy-in of tournament
    """    
    for elem in hh:
        if 'totalbuyin' in elem:
            temp = elem 
            temp = temp.replace('<totalbuyin>$', '')
            temp = temp.replace('</totalbuyin>', '')
            return float(temp)


def gametype(hh):
    """gets gametype of tournament - used to get 'cash_or_tourn', which may be a misleading name 

    Args:
        hh: 'HandHistory' column, list string data of hand

    Returns:
        string: type of game
    """    
    temp = None
    for elem in hh:
        if 'gametype' in elem:
            temp = elem.replace('<gametype>', '').replace('</gametype>', '').strip()
            break
    return temp




def hole_cards(hh):
    """finds the cards I hold, saves the 2 values in their present form to a list

    Args:
        hh: 'HandHistory' column, string data of hands

    Returns:
        list: 2 cards I held, Suit:Face Value format
    """    

    c1 = ''
    c2 = ''
    for elem in hh:
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


def start_stack(hh): 
    """Finds amount of chips I started hand with

    Args:
        hh: 'HandHistory' column, string data of hands

    Returns:
        float: number of chips
    """    

    result = None
    temp = ''
    for elem in hh:
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

def tournament_type(hh):
    """gets type of tournament


    Args:
        hh:'HandHistory' column,  string data of hands

    Returns:
        string: tournament type
    """
    result = ''
    cut = 0
    counter = 0
    for elem in hh:
        if '<tournamentname>' in elem: # doing some string wrangling below to get just the name of the tournament
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

def won(hh):
    """How much I won in the hand

    Args:
        hh:'HandHistory' column,  string data of hands

    Returns:
        float: amount won
    """

    won = ''
    temp = ''
    result = 0
    for elem in hh:
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


def bet(hh):
    """finds amount I bet in the hand 

    Args:
        hh: 'HandHistory' column, string data of hands

    Returns:
        float: amount bet
    """

    bet = ''
    temp = ''
    result = None
    for elem in hh:
        if 'Hero' in elem and 'addon' in elem:
            temp = elem
    
    if temp != '':
        temp = temp.split(' ')
        for elem in temp:
            if 'bet' in elem:
                bet = elem.replace('bet="', '').replace('"', '')
                result = float(bet)
    return result 

def total_players(hh):
    """finds number of total players at table

    Args:
        hh: 'HandHistory' column, string data of hands

    Returns:
        int: total number of players (2-9 should be possible values)
    """

    count = 0
    for elem in hh:
        if 'Pocket' in elem:
            count += 1
    return count 


def position(hh):
    """Finds where I was seated 

    Args:
        hh: 'HandHistory' column, string data of hands

    Returns:
        float: My position where 1 is the earliest seat and the total number of players would be equal to the last seat
        (e.g. if there are three players, and I am sitting in the earliest position, return = 1/3 or 0.33)
    """

    pos_lst = []
    dealer_pos = 0
    dealer_exists = False
    hero_counter = 0
    hero_found = False
    result = None 
    hero_pos = 0
    SB = ''
    for elem in hh: # find all initial seatings
        if 'dealer' in elem:
            pos_lst.append(elem)

            
    for idx, elem in enumerate(pos_lst):
        if 'dealer="1"' in elem:
            dealer_pos = idx
            dealer_exists = True
            break
        
    if dealer_exists == False:
        for elem in hh:
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

    
def table_max(hh):
    """max number of seats at the table, always greater or equal to number of players at table

    Args:
        hh:'HandHistory' column,  string data of hands

    Returns:
        int: max players
    """
    result = None
    for elem in hh:
        if 'maxplayers' in elem:
            result = int(elem.replace('<maxplayers>', '').replace('</maxplayers>',''))
            break
    return result 



def my_blind_anti_total(hh):
    """Finds how much I put in in blinds/anti

    Args:
        hh:'HandHistory' column,  string data of hands

    Returns:
        float: amount blinded or antied 
    """
    action_list = []
    result = 0
    for elem in hh:
        if '[cards]' in elem and 'Hero' in elem:
            action_list.append(elem)
    for elem in action_list:
        for sub_string in elem.split():
            if 'sum' in sub_string:
                result += float(sub_string.replace('sum="', '').replace('"', '').strip())
    return result 



def bets_before_my_preflop_action(hh):
    """Finds amount bet prior to my preflop action (total sum of)

    Args:
        hh:'HandHistory' column,  string data of hands

    Returns:
        float: amount opponents bet before my action
    """
    
    start = 0
    stop = 0
    total=0
    subset = []
    for idx, elem in enumerate(hh): # find beginning/end of preflop action
        if 'Pocket' in elem:
            start = idx
        if '<round no="2">' in elem: # WILL probably have to change this for instances when there was no round2
            stop = idx
            break 
    if stop != 0:
        subset = hh[start+1:stop-1] 
        for idx, elem in enumerate(subset): # iterates through subset to find my first action 
            if 'Hero' in elem:
                subset = subset[:idx]
                break 
        for elem in subset:
            for elem in elem.split():
                if 'sum' in elem:
                    total += float(elem.replace('sum="', '').replace('"',''))
    
    return total
        

def action_type(hh):
    """types of actions a player made preflop, 

    Args:
        hh:'HandHistory' column,  string data of hands

    Returns:
        dictionary: dictionary with the actions all players took in hand according to types as determined by DriveHud
    """    


    result = {}
    start = 0
    stop = 0
    player = None
    action_type = None 
    for idx, elem in enumerate(hh): # finds start of preflop action 
        if 'Pocket' in elem:
            start = idx
    subset = hh[start+1:]
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



def player_names(hh):
    """gets names of all the players in hand

    Args:
        hh:'HandHistory' column,  string data of hands

    Returns:
        list: all of the players in hand as string values
    """    
    player = None
    result = []
    for elem in hh:
        if 'dealer' in elem: 
            for sub_elem in elem.split(): # finds lines where player names are specified 
                if 'name' in sub_elem:
                    player = sub_elem.replace('name="', '').replace('"', '')
                    result.append(player)
                    break 
    return result 


def players_before(hh):
    """ finds all players having entered hand before my action (acted but didn't fold)

    Args:
        hh:'HandHistory' column,  string data of hands

    Returns:
        list: string values of all players having entered hand before my first action
    """    
    start = 0
    stop = 0
    players_before = [] # list of players before
    for idx, elem in enumerate(hh): # list of players after 
        if 'Pocket' in elem:
            start = idx
    subset = hh[start+1:] # subset containing preflop action until end
    for idx, elem in enumerate(subset):
        if '</round>' in elem:
            stop = idx
            break 
    subset = subset[:stop] # subset containing just preflop action 
    for elem in subset:
        action_type = 0
        if 'Hero' in elem: # break if we find hero 
            break
        else:
            for sub_elem in elem.split():
                if 'player' in sub_elem:
                    player_name = sub_elem.replace('player="', '').replace('"', '')
                if 'type' in sub_elem:
                    action_type = int(sub_elem.replace('type="', '').replace('"', ''))
            if action_type!= 0:
                players_before.append(player_name)
    return players_before

def players_after(hh):
    """finds players acting after me in hand (discludes players who have already made 1st action)

    Args:
        hh:'HandHistory' column,  string data of hands

    Returns:
        set: all the players acting after me 
    """    
    start = 0
    stop = 0
    hero_found = False
    players_before = set() # set of players before
    players_after = set() # set of players after 
    for idx, elem in enumerate(hh): 
        if 'Pocket' in elem:
            start = idx
    subset = hh[start+1:] # subset containing preflop action until end
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

def limpers(hh):
    """counts number of limpers prior to my first action 

    Args:
        handhistory:'HandHistory' column,  string data of hands

    Returns:
        int: number of players having limped
    """    
    count = 0
    for idx, elem in enumerate(hh): 
        if 'Pocket' in elem:
            start = idx
    subset = hh[start+1:] # subset containing preflop action until end
    for idx, elem in enumerate(subset):
        if '</round>' in elem:
            stop = idx
            break 
    subset = subset[:stop] # subset containing just preflop action 
    for elem in subset:
        if 'Hero' in elem or ('type="3"' not in elem and 'type="0"' not in elem): # breaks if action arrives to me OR someone doesn't limp/fold
            break 
        else:
            if 'type="3"' in elem:
                count += 1
    return count 

def raises_and_reraises(hh): # pretty sure this works but consider checking to make sure 
    """returns 1 if there was a raise, and 1 + n for ever n reraise after

    Args:
        hh:'HandHistory' column,  hand history from apply function above - string data of hands

    Returns:
        int: number of raises and reraises that occured prior to my first action 
    """    
    bet = 0
    player_name = 0
    player_amount_bet = {} # store amount bet to delineate shoves from calls (all shoves are shoves but some are raises and some are calls)       
    for elem in hh: # getting amount blinded/antied prior to betting
        if '[cards]' in elem and ('type="1"' in elem or 'type="2"' in elem): # ignores antis  
            for sub_string in elem.split():
                if 'player' in sub_string: # get player name
                    player_name = sub_string.replace('player="', '').replace('"', '') 
                if 'sum' in sub_string: # get amount blinded/antied
                    bet = float(sub_string.replace('sum="', '').replace('"', '')) 
                player_amount_bet[player_name] = bet # add player name as key and bet as value to dictionary
                            
    for idx, elem in enumerate(hh): # find beginning of pre-flop action
        if 'Pocket' in elem:
            start = idx
    subset = hh[start+1:] # subset containing preflop action until end
    for idx, elem in enumerate(subset): # find end of preflop action
        if '</round>' in elem:
            stop = idx
            break 
    subset = subset[:stop] # subset containing just preflop action   
    
    count = 0 # variable to count the number of raises/reraises
    for elem in subset:

        if 'Hero' in elem: # ends process if action arrives to me
            break
        else:
            if 'type="23"' in elem or 'type="7"' in elem: # finds shoves & raises
                for sub_string in elem.split(): # gets amount shoved/raised & players name
                    if 'player' in sub_string:
                        player_name = sub_string.replace('player="', '').replace('"', '') 
                    if 'sum' in sub_string:
                        bet = float(sub_string.replace('sum="', '').replace('"', ''))  
                if bet > max(player_amount_bet.values()): # finds whether bet was bigger than a call (type 7 is shove, which isn't necessarily a raise)
                    count += 1
                if player_name in player_amount_bet: # adds player bet to amount from blinds
                    player_amount_bet[player_name] += bet
                else:
                    player_amount_bet[player_name] = bet
    return count 

def callers(hh): # pretty sure this works but consider checking to make sure 
    """number of players to have made a call - PROBABLY COULD USE ADDITIONAL CLEANUP

    Args:
        hh:'HandHistory' column,  string data of hands

    Returns:
        int: number of callers, only non-0 when there has been a raise and a subsuquent call 
    """
    bet = 0
    player_name = 0
    player_amount_bet = {} # store amount bet to delineate shoves from calls (all shoves are shoves but some are raises and some are calls)       
    for elem in hh: # getting amount put in prior to betting
        if '[cards]' in elem and ('type="1"' in elem or 'type="2"' in elem): # ignores antis  
            for sub_string in elem.split():
                if 'player' in sub_string:
                    player_name = sub_string.replace('player="', '').replace('"', '') 
                if 'sum' in sub_string:
                    bet = float(sub_string.replace('sum="', '').replace('"', '')) 
                player_amount_bet[player_name] = bet
                            
    for idx, elem in enumerate(hh): 
        if 'Pocket' in elem:
            start = idx
    subset = hh[start+1:] # subset containing preflop action until end
    for idx, elem in enumerate(subset):
        if '</round>' in elem:
            stop = idx
            break 
    subset = subset[:stop] # subset containing just preflop action   
    
    raise_happened = False # trigger for when a raise occures 
    count = 0
    for elem in subset:

        if 'Hero' in elem:
            break

        for sub_string in elem.split(): # gets amount shoved or raised & players name
            if 'player' in sub_string:
                player_name = sub_string.replace('player="', '').replace('"', '') 
            if 'sum' in sub_string:
                bet = float(sub_string.replace('sum="', '').replace('"', ''))            

        if ('type="23"' in elem or 'type="7"' in elem) and raise_happened == False: # finds shoves & raises, trying to avoid edge cases here but probably some extraneous stuff

            if 'type="7"' in elem:
                if bet > max(player_amount_bet.values()):# checks to see if shove was a raise or call 
                    raise_happened = True
            else: # for raises
                raise_happened = True

                
        if raise_happened:
            if 'type="3"' in elem:
                count += 1
            if 'type="7"' in elem:
                if bet <= max(player_amount_bet.values()):
                    count += 1
        if player_name not in player_amount_bet:
            player_amount_bet[player_name] = bet
        else:
            player_amount_bet[player_name] += bet
    return count 

