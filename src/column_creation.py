import pandas as pd
import sqlite3
pd.set_option("display.max_columns", 100)
import numpy as np

def load_df():
    conn = sqlite3.connect("/home/sam/Documents/DSI/capstone/poker/data/drivehud.db")
    hand_history = pd.read_sql_query("select * from HandHistories;", conn)
    hand_history.HandHistory = hand_history.HandHistory.str.split('\r\n')

    df = hand_history.copy()

    return df 


def fill_columns(df, fill_BB_nans = False):
    df['buyin'] = df['HandHistory'].apply(lambda row: buyin(row)) 

    df['gametype'] = df['HandHistory'].apply(lambda x: gametype(x))

    df['my_blind_anti_total'] = df.HandHistory.apply(lambda x: my_blind_anti_total(x))

    df['the_deck'] = df['HandHistory'].apply(lambda row: possible_cards(row))

    df['my_cards'] = df['HandHistory'].apply(lambda row: hole_cards(row))
    
    df['blinds'] = df.apply(lambda x: blinds(x), axis =1)

    df['starting_stack'] = df['HandHistory'].apply(lambda row: start_stack(row))
    
    df['tournament_type'] = df['HandHistory'].apply(lambda row: tournament_type(row))

    df['won'] = df['HandHistory'].apply(lambda row: won(row))

    df['bet'] = df['HandHistory'].apply(lambda row: bet(row))
    
    df['made_money'] = df['won'] > df['bet']
    
    df['made_money'] = df['made_money'].apply(lambda x: fix_made_money(x))
    
    df['total_players'] = df['HandHistory'].apply(lambda x: total_players(x))
    
    df['card_rank'] = df['my_cards'].apply(lambda x: cards_numeric(x))
    
    df['position'] = df['HandHistory'].apply(lambda x: position(x))
    
    df['BB'] = df['blinds'].apply(lambda x: BB(x))
    
    if fill_BB_nans == True:
        df = fix_BB_nans(df) # consider removing? # way I did this causes a warning 
    
    df['BB_in_stack'] = df.apply(lambda x: BB_in_stack(x['starting_stack'], x['BB']), axis = 1)

    df['net_outcome'] = df['won'] - df['bet'] 

    df['all_in'] = df.apply(lambda x: all_in(x['starting_stack'], x['bet']), axis = 1)

    df['money_beyond_blind'] = df.apply(lambda x: money_beyond_blind(x), axis = 1) # whether i put in money in addition to OG blind

    df['hour'] = df['HandHistoryTimestamp'].apply(lambda x: pd.to_datetime(x).hour) # will need to determine degree to which time is offset

    df['year_month_day'] = pd.to_datetime(df['HandHistoryTimestamp']).dt.to_period('D').dt.to_timestamp()  # will need to determine degree to which time is offset

    df['days_since_start'] = df['year_month_day'].apply(lambda x: (x - pd.to_datetime('2019-10-24 00:00:00')).days)

    f_dic = frequency_dict(df)

    df['hand_frequency'] = df['days_since_start'].apply(lambda x: hand_frequency(x, f_dic))

    # using bet to describe putting any amount of $ in the pot 
    df['flop_bet'] = df.apply(lambda x: flop_bet(x), axis = 1)

    df['turn_bet'] = df.apply(lambda x: turn_bet(x), axis = 1)

    df['river_bet'] = df.apply(lambda x: river_bet(x), axis = 1)

    df['preflop_bet'] = df['bet'] - (df['flop_bet'] + df['turn_bet'] + df['river_bet'] + df['my_blind_anti_total'])

    df['high_card'] = df['my_cards'].apply(lambda x: high_card(x))

    df['suited'] = df['my_cards'].apply(lambda x: suited(x))

    df['pocket_pair'] = df['my_cards'].apply(lambda x: pocket_pair(x)) # redundant with the gap column?

    df['gap'] = df['my_cards'].apply(lambda x: gap(x))

    df['low_card'] = df['my_cards'].apply(lambda x: low_card(x)) # redundant with gap/high card? 

    df['table_max_players'] = df['HandHistory'].apply(lambda x: table_max(x))

    return df


########################################################################################

# functions we will be applying to above 




# lambda function to turn OG 'made_money' column into 1 - 0 boolean (instead of boolean)
def fix_made_money(x):
    result = 0
    if x == True:
        result = 1
    else:
        result = 0
    return result

# looking at players at table or players in hand????
def total_players(x):
    count = 0
    for elem in x:
        if 'Pocket' in elem:
            count += 1
    return count 

def buyin(x): # this seems to work, the implementation is functionalized above 
    for elem in x:
        if 'totalbuyin' in elem:
            temp = elem 
            temp = temp.replace('<totalbuyin>$', '')
            temp = temp.replace('</totalbuyin>', '')
            return float(temp)

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
    
# probably uneccesary 
def possible_cards(x): # will do this first, and then remove cards in seperate functions, still not sure how to deal with all in vs seeing later action
    deck = []
    for s in ['D', 'S', 'C', 'H']:
        for c in ['2','3','4', '5', '6', '7', '8', '9', '1', 'J', 'Q', 'K', 'A']: # making 10 just 1 for consistency sake
            temp = s + c
            deck.append(temp)
    return deck 




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


# some tournaments just labeled 'holdem, at somepoint try to figure out what these are
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

# maybe recycle some of this code in order to get dummy columns for certain types of hands?
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
            
#def bb_in_stack(x):

# get BB out of this one? not the actual BB, just if i am the BB 
def position(x):
    pos_lst = []
    dealer_pos = 0
    dealer_exists = False
    hero_counter = 0
    hero_found = False
    result = None 
    hero_pos = 0

    for elem in x: # find all initial seatings
        if 'dealer' in elem:
            pos_lst.append(elem)

            
    for idx, elem in enumerate(pos_lst):
        if 'dealer="1"' in elem:
            dealer_pos = idx
            dealer_exists = True
            break
        
    if dealer_exists:
        if dealer_pos != len(pos_lst) - 1:
            beginning = pos_lst[dealer_pos + 1 : ]
            rest = pos_lst[ : dealer_pos + 1]
            for elem in beginning:
                if 'name="Hero"' in elem:
                    hero_counter += 1
                    hero_pos = hero_counter
                    hero_found = True
                    break 
                else:
                    hero_counter += 1
            if hero_found == False:
                for elem in rest:
                    if 'name="Hero"' in elem:
                        hero_counter += 1
                        hero_pos = hero_counter
                        hero_found = True
                        break
                    else:
                        hero_counter += 1
        else:
            for elem in pos_lst:
                if 'name="Hero"' in elem:
                    hero_counter += 1
                    hero_pos = hero_counter
                    hero_found = True
                    break
                else:
                    hero_counter += 1
    
    if hero_found:
        result = hero_pos / len(pos_lst)
    
    return result




def BB(x): # did this super jankily, definitely return. just wanna see if i can get this loosely working
  

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


# maybe create a few ranges? I'll leave it like so for now and then replicate as needed 

def frequency_dict(df): # hands played in 15 day period (7 days before, current day, 7 days after)
    result = {}
    date_range = np.array([-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7]) # maybe change this to an argument 
    last_day = df['days_since_start'].iloc[-1] # get last day's day number
    day = 0
    while date_range[7] <= last_day: 
        day_count = 0 # counts number of hands for that given hands day range

        for num in date_range:
            mask = df['days_since_start'] == num
            day_count += df[mask].shape[0]
        result[day] = day_count
        day += 1
        date_range +=1
    return result

def hand_frequency(x, dic): # uses dictionary created from above to assign a value to each row 
    return dic[x]

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

def gametype(x):
    temp = None
    for elem in x:
        if 'gametype' in elem:
            temp = elem.replace('<gametype>', '').replace('</gametype>', '').strip()
            break
    return temp


def blinds(x): # hand history & gametype 
    gt = x['gametype']
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

def table_max(x):
    result = None
    for elem in x:
        if 'maxplayers' in elem:
            result = int(elem.replace('<maxplayers>', '').replace('</maxplayers>',''))
            break
    return result 

# possibly unecessary now that we know that most of our BB nans were from cash games 

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

#####################################################################################################################################

# not a column function, just something to reduce the series for regression purposes
def X_y_regression(df):
    X = df[['buyin', 'card_rank', 'BB_in_stack', 'position', 'net_outcome']]

    X = X.dropna()

    y = X.pop('net_outcome')

    return X, y

def split_cash(df):
    tourn_mask = df['gametype'] == 'Holdem NL'
    cash_mask = df['gametype'] != 'Holdem NL'
        
    cash = df[cash_mask]
    tourn = df[tourn_mask]
    
    return tourn, cash 

if __name__ == "__main__":
    df = load_df()

    df = fill_columns(df,fill_BB_nans=True)

    
    df.to_csv('full_dataframe.csv')













































































































































    