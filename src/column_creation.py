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


def fill_columns(df):
    df['buyin'] = df.HandHistory.apply(lambda row: buyin(row)) 

    df['the_deck'] = df.HandHistory.apply(lambda row: possible_cards(row))

    df['my_cards'] = df.HandHistory.apply(lambda row: hole_cards(row))
    
    df['blinds'] = df.HandHistory.apply(lambda row: blinds(row))

    df['starting_stack'] = df.HandHistory.apply(lambda row: start_stack(row))
    
    df['tournament_type'] = df.HandHistory.apply(lambda row: tournament_type(row))

    df['won'] = df.HandHistory.apply(lambda row: won(row))

    df['bet'] = df.HandHistory.apply(lambda row: bet(row))
    
    df['made_money'] = df['won'] > df['bet']
    
    df['made_money'] = df.made_money.apply(lambda x: fix_made_money(x))
    
    df['total_players'] = df.HandHistory.apply(lambda x: total_players(x))
    
    df['card_rank'] = df.my_cards.apply(lambda x: cards_numeric(x))
    
    df['position'] = df.HandHistory.apply(lambda x: position(x))
    
    df['BB'] = df.blinds.apply(lambda x: BB(x))
    
    df['BB_in_stack'] = df.apply(lambda x: BB_in_stack(x['starting_stack'], x['BB']), axis = 1)

    df['net_outcome'] = df['won'] - df['bet'] 

    df['all_in'] = df.apply(lambda x: all_in(x['starting_stack'], x['bet']), axis = 1)

    df['money_beyond_blind'] = df.apply(lambda x: money_beyond_blind(x['HandHistory'], x['bet']), axis = 1) # whether i put in money in addition to OG blind

    df['hour'] = df['HandHistoryTimestamp'].apply(lambda x: pd.to_datetime(x).hour) # will need to determine degree to which time is offset

    df['year_month_day'] = pd.to_datetime(df['HandHistoryTimestamp']).dt.to_period('D').dt.to_timestamp()  # will need to determine degree to which time is offset

    df['days_since_start'] = df['year_month_day'].apply(lambda x: (x - pd.to_datetime('2019-10-24 00:00:00')).days)

    f_dic = frequency_dict(df)

    df['hand_frequency'] = df['days_since_start'].apply(lambda x: hand_frequency(x, f_dic))

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


def blinds(x):
    blind_list = []
    result = []
    for elem in x:
        if '[cards]' in elem:
            blind_list.append(elem)
    for elem in blind_list:
        temp = elem.split(' ')
        for s in temp:
            if 'sum' in s:
                temp2 = s.replace('sum="', '')
                temp2 = temp2.replace('"', '')
                result.append(float(temp2))
    return result 

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
    
    for elem in x:
        if 'dealer' in elem:
            pos_lst.append(elem)

            
    for idx, elem in enumerate(pos_lst):
        if 'dealer="1"':
            dealer_pos = idx
            dealer_exists = True
        
    if dealer_exists:
        if dealer_pos < len(pos_lst) - 1:
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
  
    def look_for_blinds(blinds):
        result = None 
        if len(blinds) == 2:
            if max(blinds) / min(blinds) == 2:
                result = max(x)


        else:
            if len(blinds) > 2:
                BB = blinds.pop(blinds.index(max(blinds)))
                SB = blinds.pop(blinds.index(max(blinds)))
                anti = blinds.pop(blinds.index(max(blinds)))
                if BB / SB == 2 and BB / anti == 10:
                    result = max(x)



        return result 

    result = look_for_blinds(x)

    
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




def money_beyond_blind(HH, bet):
    temp = None
    blind = None
    result = 0
    for elem in HH:

        if 'cards="[cards]"' in elem and 'Hero' in elem:
            temp = elem.split()
            break
    if temp != None:
        for elem in temp:
            if 'sum=' in elem:
                blind = float(elem.replace('sum="', '').replace('"', '').strip())
                break
    if blind != None and bet != None:
        if blind < bet:
            result = 1

    return result




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











# not a column function, just something to reduce the series for regression purposes
def X_y_regression(df):
    X = df[['buyin', 'card_rank', 'BB_in_stack', 'position', 'net_outcome']]

    X = X.dropna()

    y = X.pop('net_outcome')

    return X, y



if __name__ == "__main__":
    df = load_df()

    df = fill_columns(df)

    
    print(df.info()) 
    print(df.tail(5))
    print(df.head(5))













































































































































    