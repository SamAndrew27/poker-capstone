# Predicting Poker Hand Outcomes

![Hud Image](/images/cap2_images/table.PNG)

## Goal

The goal of this project is to use a database of all the online poker hands I have played since October 2019 to build a model that predicts whether I should or should not play any given hand. Because poker is partly a game of luck, the goal here is not perfection, but rather a model that helps guide my decision making.  


## Background
My first experience with poker was at my grandparents’ house. It was a family affair with all my aunts, uncles, great-aunts, great-uncles, etc. playing for nickels around the dining room table. I didn’t often win, but when I did, it was probably the result of kindness rather than my own savvy. What I did gain from those family evenings was a love of the game. 

In high school I dabbled in online bitcoin poker, but it wasn’t until college that I began to play on a regular basis. During my junior year, my housemates and I played Texas Hold’em a few times per week. I was by no means the best player, but I enjoyed it as much as anyone. 

After college, I once again started playing bitcoin poker, but I decided to stop for a few reasons. I was a recreational player with limited knowledge of the game, and bitcoin prices were getting scary high. I became uncomfortable with the bitcoin stakes, and so I began to play on a site that used good old American dollars as its metric. This site also allowed something that the bitcoin site did not, a HUD display. A HUD display records all the actions each player makes, and also tracks how much money you are earning or losing. I hope to use the HUD database to determine the expected outcome of any given poker hand.


## The Data 
The data is stored in several SQL databases, but to limit the scope of the project I decided to focus on the database that contained a record of every individual hand of poker I had played. It contained over fifty thousand rows, each representing a single hand of poker. For each of these data points there were seven columns, but the one that caught my eye was the HandHistory column, which contained the progression of every poker hand, stored as a single string. After the strings were split so that they could be more easily interpreted, they looked like this: 
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
From this data I hoped to build a model to predict the outcome of any given hand. The original 53 thousand rows contained cash hands as well as tournament hands. I won’t get into the differences here, but cash games are different from tournaments. I therefore elected to focus on the ~40k tournament hands at my disposal. Given the nature of my problem, there was little value in looking at the hands I didn’t play, as there was no outcome on which to train my model. I decided to look only at the hands where I wagered beyond what I was required to ante before any cards were dealt. This left me with a total of 10,695 hands, 20% of which were put into a holdout set. 

## Feature Creation

* Position: this is my position at the table, as a fraction of the total players. In early position, you have to make your bet first, which generally puts you at a disadvantage relative to those who make their play after you. If I am in the dealer position, the latest possible position, the value for this feature is a 1. If I am in the small-blind, the earliest possible position, its value can be as low as 0.11.

* Big Blinds in Stack: this is how much money I have, relative to the Big Blind. The Big Blind is the amount one player has to bet before any cards are dealt. It generally represents the minimum size of the bet as well. This ratio heavily dictates the strategy a poker player ought to follow in a tournament game.
![BB in stack plot](/images/general-plots/bb_in_stack_all_data.PNG)

* Suited: whether the two cards in my hand were of the same suit, represented by a boolean value of 1 for suited and 0 for unsuited. Having two cards of the same suit makes it easier to make flushes, one of the better possible Texas Hold’em hands.  

* Low Card: the lowest card in my hand, represented by an integer value. Values in this category range from 2, representing a 2, to 14, representing an ace.

* High Card: the highest card in my hand, represented by an integer value, the same as “Low Card.” In the case that the high card is equal to the low card (i.e. a pocket pair) they will both have the same value.

* Card Rank: using a formula created by Bill Chen, a professional poker player with a degree in mathematics, I wanted to create a value to represent the strength of my hand. These values range from -1 for 7-2, the worst possible hand, to 20 for pocket aces, the strongest possible hand.
![Card Rank](/images/general-plots/card_rank_all_data.PNG)

* Limpers: If a poker player puts in the minimum amount required to continue playing their hand their action is known as a “limp.” There are different theories about how often a poker player ought to do this. It was previously believed that limping is a hallmark of a weak poker player, and that good poker players nearly always raised when they planned on playing a hand. Solvers have changed the thinking about limping to some degree, especially for tournament poker. There are situations when it is correct to limp, but it is still usually done by weak poker players at a higher frequency. This feature is an integer value representing the number of limps that occurred prior to my decision point, and for my dataset these values range from 0 to 6.

* Raises & Re-raises: When a player puts in more than the required amount this is known as a raise. A re-raise is when a subsequent player repeats this process. A raise, and especially a re-raise, is a sign of strength. This feature represents the number of raises and re-raises that have occurred prior to the action coming to me. For my dataset these values ranged from 0 to 3. 
![raises&reraises](/images/general-plots/raises_all_data.PNG)

* Number of Players Before: This feature denotes the number of players who have entered the hand. It will never be smaller than the sum of limpers and raises/reraises, as all those players have entered the hand. It may also include players who just called (put in the minimum) after a raise or re-raise was made. It is an integer value that ranges from 0 to 6 for my dataset. The preferred size of this number varies according to table conditions. If you have a very strong hand you might be happy to see that a lot of players have put in money, but with more marginal holdings you may prefer to fight for the pot amongst a smaller subset of players;
![num_players_before](/images/general-plots/number_of_players_all_data.PNG)

* Number of Players After: This feature represents the number of players yet to make their first action. It is an integer value, and its value ranges from 0 to 8. You usually prefer to see a lower number here, but confounding variables make it tricky to say outright that a lower number is preferable. 

* Made or Lost Money: My target variable. It is a boolean value, with the positive class representing situations in which I made money or broke even and the negative class representing situations in which I lost money.
![Won vs Lost](/images/general-plots/won_v_lost_all_data.PNG)




## Expectations & Modeling Goals

Before I discuss modeling, it should be noted that there is much variance intrinsic to the game of poker. This is especially true of tournament poker, where often only 10-20% of the players walk away with cash in their pocket. Even very good tournament poker players will have long losing streaks. A simulation from Michael Acevedo’s book Modern Poker Theory found that over the course of 2000 tournaments a poker player with an average ROI of 25% can expect to lose as much as 8% of their original stake. 

This same sort of variation is also present on a hand-to-hand basis. The best possible hand, pocket aces, will beat the worst hand, 7-2 offsuit, around 87% of the time. This means that the question of whether I should play a poker hand is not the same as whether I will win a hand. Therefore my model can only hope to be a suggestion, and will not be able to perfectly predict whether or not I will win money. 


![Aces](/images/cap2_images/aces.png)

My model is built exclusively from the hands that I did play. It is possible that there are many hands that I should have, but did not play. I will not be able to answer this question unless I start playing all the hands I am dealt, which is certainly not an ideal strategy. There are many different ways to improve at poker, but my model hopes to answer one very specific and important question: given the manner in which I have historically played and given the conditions when cards are first dealt will I most likely win or lose money by playing any given poker hand. 


## Classification Modeling

I first approached this problem as a regression problem, and trained some models to predict how much I would win or lose. These models performed quite poorly. It became apparent that regression models were never going to be able to perform particularly well at the task I had given them. The amount that a player wins or loses in poker is largely a product of the cards dealt to other players, the cards that hit the felt, and the strategies of other players. I could not feed these factors into my model because they are unknown when I make my initial decision to play or fold. At this junction, I realized that I was approaching the problem in the wrong way. Rather than trying to predict how much I would win on any given hand, I elected to treat it as a classification problem. I decided to treat hands in which I made money or broke even as the positive class, and hands in which I lost money as the negative class. 

To decide what type of model to use, I considered Brier scores and ROC AUC scores to get some idea of how the models were performing with default parameters. ROC AUC captures how often a model is making the correct prediction. A Brier score is a type of cost function for classification problems, and fulfills an analogous role to what mean squared error does for regression problems. I tested Random Forest, KNN, Logistic Regression, AdaBoost, and Gradient Boost. I found that Gradient Boost performed the best across both metrics. Logistic Regression also performed well, so I decided to explore both as possible models. 

When I began tuning my models I decided to focus on the f1 score as the parameter to measure model performance, as it captured two things I wanted to explore. The first, precision, allowed me to know how much confidence I could put in a positive prediction. The second, recall, informed me of the opportunity cost of my model by factoring in the false positive rate. After tuning both my models I found that Gradient Boost performed the best with an f1 score of 0.76. Logistic regression did not perform quite as well, with an f1 score of 0.745.

I tried to build a composite model using both Logistic and Gradient Boost. I evaluated the performance of these models by looking at several metrics. There is a poker concept called ICM, and one of its principles  is that your last chip is worth a lot more than your 1,000th chip. I therefore decided to minimize the rate of false positives, as these cases would lead me to losing money, making precision my most important metric. Essentially this allows me to know how much stock I can put in a positive prediction by my model. 

I decided to also look at negative predictive value (NPV). It measures the rate of true negatives divided by the sum of true negatives and false negatives. By considering the NPV, I hoped to minimize the number of false positives, as these cases would lead to me missing out on hands that I was likely to win. For the reason stated above, however, I decided that it was secondary to precision. 

After performing 1000 cross validations on each model, I found the addition of my lesser model added very little additional predictive value. 

I also decided to attempt developing a neural network to solve my problem. While it initially seemed quite promising, after tuning both models I was not able to develop a neural network that outperformed Gradient Boost. Combining the two yielded equally fruitless results, so I decided to use Gradient Boost alone. 


### Results of Testing

Testing Gradient Boost with the default prediction threshold of 0.5 on my holdout set produced a precision of about 0.64, an NPV of 0.71, and an accuracy of 0.645. Although I was pleased with these results, I decided to set a number of different thresholds so that my model produces multiple types of predictions, rather than just a binary positive or negative. The highest threshold I set at 0.63. For any prediction above this threshold my model outputs ‘Play It!’ The second highest threshold ranges from 0.595 to 0.655, and in this range my model outputs ‘Probable Win.’ The next category includes predictions ranging from 0.51 to 0.595, and in this range my model outputs ‘Caution Zone’. In this range I have only a slightly higher chance of winning than I do losing. I should be playing some hands in this range, but must tread lightly. The final category of prediction is for any prediction below 0.51. In this range my model outputs ‘Don’t Do It!’. These are hands I tend to lose, with winning hands only making up about 30% of this grouping. 

I hope that having these different categories can help inform me which hands to play. When I receive a prediction of ‘Play It!’ I can assume that I will very likely win, given a precision of 0.77 at that threshold. The same is true for values in the ‘Probable Win’ category where these values have a precision of 0.67, meaning that I should win two thirds of these hands. The ‘Caution Zone’ is where my decision making gets dicier. With a precision of 0.52 I will win slightly over half of the hands my model predicts are in this category. I can’t simply fold all of these hands; if I did so I would be folding far too many hands that are strong enough to play. It should also be mentioned that it is typically the case that you only have to put in a fraction of your money to see the first three cards. For this reason you generally can afford to lose more hands than you win, as long as you make up for your losses when you do win. I will therefore regard the caution zone as somewhat discretionary. The last category ‘Don’t Play It!’ speaks for itself. I will win fewer than 30% of these hands, and will avoid playing them despite any unfound optimism that tells me otherwise.

The model I created will hopefully push me in the direction of becoming a better poker player. While it is far from a perfect predictor, I can use it in situations where I feel that the expected value of playing a hand is close to that of folding it. In Data Science terms, I will continue to be the primary predictive model at the poker table, but my Gradient Boosting model can serve as a secondary model that informs my decision making process. 

I also hope to be able to analyze Partial Dependence plots to help identify leaks in game. I have not yet done much serious analysis of these,  but one initial takeaway is that I tend to perform much worse when I have more big blinds in my stack. Given what I know about my playing style, this means that I am probably playing too passively when this is the case. 
![results](/images/general-plots/holdout_results_caution.png)

## Flask App
Having created my model, I wanted to package it in a format where I could feed it information and quickly get results so that I could use it while actually playing. To do this I used Flask to build a basic web page. It has the user (most likely me) plug in a number of details about their  current situation. These are then read into a Pandas DataFrame, upon which my model then performs a prediction.




## Next Steps
There are a number of avenues I could explore in order to expand upon the work done here. The first that comes to mind is looking at the situations in which my opponents showed their hands at the end of a round of poker. By doing this, I could look at how much equity I had in a hand, rather than just the net outcome after all the cards have hit the felt. My current target variable is partly a product of luck, while equity is not. At present, the small sample size of such situations available to me makes this a difficult task. One solution might be to use the poker site where I play to try to get this data. After a certain number of days it allows you to see what cards your opponent had. This would greatly increase the sample size available to me if I were able to combine that data with what I presently have. 

Another avenue I hope to explore is post flop situations. This would mean working with a smaller dataset than I have presently, but I have already created features for much of this data. A model based upon this data would hopefully allow me to improve my strategy beyond the single decision my current model aims to inform. 

I also computed some statistics on my opponents playing style. Voluntarily Put in Pot (VPIP) is a common poker statistic, and one I created for my data set. It is a percentage of the hands an opponent electively entered by putting in money, and is generally considered to be a very important statistic in poker decision making. Using all the actions my opponents previously made at the table, I computed these stats in several different forms. I found that I did not have enough hands to make VPIP useful for my current model. My hope is that it can be incorporated into my modeling in the future. 

The thing that could give my model the most utility would be to make it publicly accessible. My hope is that by building an EC2 instance I can allow other DriveHud users to upload their own databases, which will then be converted into the same format as the one my model was trained upon, allowing them to get predictions of their own. In its current form my model is only helpful to myself, but my hope is that my model could be a tool for anyone who is hoping to improve their poker game. 



