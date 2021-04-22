import numpy as np 
import pandas as pd 



def fix_val(val): # puts val in correct form
    if len(val) > 1:
        val = val[0]
    if val.isnumeric() == False:
        val = val.upper()
    return val 

def fix_suit(suit): # puts suit in correct form
    return suit[0].upper()

def construct_cards(val1, val2, suit1, suit2):
    val1 = fix_val(val1)
    val2 = fix_val(val2)
    suit1 = fix_suit(suit1)
    suit2 = fix_suit(suit2)
    card1 = f'{suit1}{val1}'
    card2 = f'{suit2}{val2}'
    cards =  [card1, card2]
    rank, suited, lc, hc = return_card_vals(cards)
    return rank, suited, lc, hc

def return_card_vals(cards):
    hc = highest_card(cards)
    lc = lowest_card(cards)
    suited = is_suited(cards)
    rank = cards_numeric(cards)
    return rank, suited, lc, hc


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
 
def highest_card(x):
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

def lowest_card(x):
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

def is_suited(x):
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
