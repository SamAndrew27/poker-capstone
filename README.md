# How Can I Become Better at Poker?

# Background
My first experience playing poker was at my grandparent’s house. It was a family affair, all my aunts, uncles, great-aunts, great-uncles, ect. would sit around the dining room table and play for nickels. I didn’t make much money, and what money I did make was probably a product of kindness rather than my own savvy. But what I did gain was a... love of the game. In highschool I played a little bitcoin poker online, but it wasn’t until college that things started to ramp up. Junior year I lived in a house with a bunch of my friends, and at least a few times a week we would convene to play Texas Hold’em. I was by no means the best, but I enjoyed it as much as anyone. After college I once again started playing bitcoin poker, but I decided to stop for a few reasons. I was a recreational player with limited knowledge of the game, and bitcoin prices were getting scary high. This meant I had to play for a lot more than I was comfortable with. So I began to play on a different site which used good old american dollars as opposed to bitcoin as its metric. This site also allowed something which the bitcoin site did not, a HUD display. A HUD display records all the actions you and your opponents make, and also tracks how much money you are earning or losing. I’m by no means a great poker player, but it is something I enjoy immensely and would like to improve at. I hope to use the HUD database at my disposal to determine what sort of hands I should play. 

# OBJECTIVE
The goal of this project is to use a database containing a history of all the poker hands I have played online since October 2019 to determine whether I should or shouldn't play any given hand. 

# The Data 
The data is stored in several SQL databases, but to limit the scope of the project I decided to focus on just one. This was the database that stored data on each individual hand of poker I had played. It contained over fifty thousand rows, each representing a single hand of poker that I played. For each of these data points there were seven columns, but the one that caught my eye was the HandHistory column, which contained the progression of every poker hand I had played, stored as a single string. After the strings were split so they could be more easily interpreted, they looked something like this: 
```python
['<session sessioncode="2297128">',
 '<general>',
 '<client_version>19.9.7.4</client_version>',
 '<uncalled_bet_enabled>false</uncalled_bet_enabled>',
 '<mode>real</mode>',
 '<gametype>Holdem NL</gametype>',
 '<tablename>Hyper Turbo (500 Chips) (#40065723)</tablename>',
 '<duration>N/A</duration>',
 '<gamecount>0</gamecount>',
 '<startdate>2021-02-04 04:16:37</startdate>',
 '<currency>USD</currency>',
 '<nickname>Hero</nickname>',
 '<bets>0</bets>',
 '<wins>0</wins>',
 '<chipsin>0</chipsin>',
 '<chipsout>0</chipsout>',
 '<ipoints>0</ipoints>',
 '<statuspoints>0</statuspoints>',
 '<awardpoints>0</awardpoints>',
 '<tournamentcode>40065723</tournamentcode>',
 '<tournamentname>Hyper Turbo (500 Chips) (#40065723)</tournamentname>',
 '<place>6</place>',
 '<buyin>$1+$0.05</buyin>',
 '<totalbuyin>$1.05</totalbuyin>',
 '<win>0</win>',
 '<maxplayers>6</maxplayers>',
 '<pokersite>Ignition</pokersite>',
 '</general>',
 '<game gamecode="4249936856">',
 '<general>',
 '<startdate>2021-02-04 04:21:01</startdate>',
 '<players>',
 '<player seat="1" name="P5_671793XV" chips="840" dealer="0" win="0" bet="0" rebuy="0" addon="0" />',
 '<player seat="2" name="P2_414718AT" chips="460" dealer="0" win="965" bet="460" rebuy="0" addon="0" />',
 '<player seat="3" name="Hero" chips="790" dealer="0" win="330" bet="790" rebuy="0" addon="0" />',
 '<player seat="5" name="P3_826370HL" chips="410" dealer="0" win="0" bet="15" rebuy="0" addon="0" />',
 '<player seat="6" name="P1_719096MR" chips="500" dealer="0" win="0" bet="30" rebuy="0" addon="0" />',
 '</players>',
 '</general>',
 '<round no="0">',
 '<action no="1" player="P3_826370HL" type="1" sum="15" cards="[cards]" />',
 '<action no="2" player="P1_719096MR" type="2" sum="30" cards="[cards]" />',
 '</round>',
 '<round no="1">',
 '<cards type="Pocket" player="P5_671793XV">X X</cards>',
 '<cards type="Pocket" player="P2_414718AT">D6 S6</cards>',
 '<cards type="Pocket" player="Hero">DQ CA</cards>',
 '<cards type="Pocket" player="P3_826370HL">X X</cards>',
 '<cards type="Pocket" player="P1_719096MR">X X</cards>',
 '<action no="3" player="P5_671793XV" type="0" sum="0" cards="" />',
 '<action no="4" player="P2_414718AT" type="7" sum="460" cards="" />',
 '<action no="5" player="Hero" type="7" sum="790" cards="" />',
 '<action no="6" player="P3_826370HL" type="0" sum="0" cards="" />',
 '<action no="7" player="P1_719096MR" type="0" sum="0" cards="" />',
 '</round>',
 '<round no="2">',
 '<cards type="Flop" player="">DJ C9 D9</cards>',
 '</round>',
 '<round no="3">',
 '<cards type="Turn" player="">C10</cards>',
 '</round>',
 '<round no="4">',
 '<cards type="River" player="">D3</cards>',
 '</round>',
 '</game>',
 '</session>']
```
From this data I hoped to create something that could build a model upon to predict the outcome of any given hand. The original 53 thousand rows contained cash hands as well as tournament hands. I won’t get too deep into the differences here, but cash games are effectively different than tournaments, so I elected to just focus on the ~40k cash hands at my disposal.

# Feature Creation
When I began this process I didn’t know exactly what I wanted to do with the data at my disposal, so I just began creating columns for anything that I thought might be useful for my project. Ultimately I created 33 different features, some of which I didn’t use at all, and some which may have utility down the road. For this project I decided to focus on just 12 variables:

Buy-in: this feature represents the amount I paid to enter the tournament. 

Total-players: The number of players in the hand. These numbers range from 2-9

Position: This feature represents the position I was in at the table, as a fraction of the total players. In early position you have to make your bet first, which generally puts you at a disadvantage to those who get to make their play after you. If I am in the dealer position, the latest possible position, the value for this feature is a 1. If I am in the small-blind, the earliest possible position, its value can be as low as .11 

Big Blinds in Stack: This feature represents how much money I have, relative to the Big Blind. The Big Blind is the amount one player has to put in prior to any cards being dealt. It generally represents the minimum size of the bet as well. This ratio heavily dictates the strategy a poker player ought to follow in a tournament game. 

Suited: Whether the two cards in my hand were of the same suit, represented by a boolean value of 1 for suited and 0 for unsuited. Having two cards of the same suit makes it easier to make flushes, one of the better possible texas holdem hands.  

Low Card: the lowest card in my hand, represented by an integer value. Values in this category range from 2, representing a 2, to 14, representing an ace 

High Card: the highest card in my hand, represented by an integer value, the same as “Low Card”

Card Rank: Using a formula created by Bill Chen, a professional poker player with a degree in mathematics, I wanted to create a value to represent the strength of my hand. These values range from -1 for 7-2, the worst possible hand, to 20 for pocket Aces, the strongest possible hand. 

## TARGET VARIABLE
Net Outcome: This feature is the amount I won or lost in respect to my starting stack, as a float. A value of 0 means I lost all my chips, and values between 0 and 1 mean I lost some amount of the chips I had to start with. For example, if I had 100 chips, and this value is 0.95, that would mean I lost 5 chips. Values greater than 1 mean I made some amount of money. It's possible that these values could be as high as 9, but in practice are rarely higher than 2 or 3. 

ADD FEATURE FOR $ at my disposal for other players in hand???
(may be more complicated than it sounds)

Fill in time columns???!?!!!?


# The Model
To determine what sort of models would be best for predicting the outcome of any given hand I designed a function to run through 7 different models, Ridge, Lasso, KNN, Random Forest, AdaBoost, XDGBoost, and Gradient Boost. I also wanted to see how much predictive value my time related features had for these various models, so I cycled through all possible combinations of them, as well as all possible exclusions. I used adjusted-R2 to measure the value of these features, and found that their inclusion generally reduced the predictive value of the models.

I used R2 as my metric to compare different models. To my surprise I found that Ridge and Lasso performed the best, followed by Gradient Boost. I started by tuning Ridge and Lasso, as well as Elastic, and found that Ridge regression performed the best, but not significantly better than it had with default parameters. I next turned to Gradient Boost. With parameter tuning I was able to get a gradient boost model which outperformed Ridge by about a factor of 3
