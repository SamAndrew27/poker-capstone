# How Can I Win More Poker Hands (and lose less)?

### Me Winning at Poker
![Hud Image](/images/table.PNG)

## Goal

The goal of this project is to use a database containing all the poker hands I have played online since October 2019 to build a model that predicts whether I should or should not play any given hand. Due to poker being partly a game of luck, the goal here is not perfection, but rather to create a model that helps guide my decision making. 


## Background
My first experience with poker was at my grandparents’ house. It was a family affair with all my aunts, uncles, great-aunts, great-uncles, etc. playing for nickels around the dining room table. I didn’t often win, but when I did, it was probably the result of kindness rather than my own savvy. But what I did gain was a love of the game. 

In high school I dabbled in online bitcoin poker, but it wasn’t until college that I began to play on a regular basis. During my junior year, my housemates and I played Texas Hold’em a few times per week. I was by no means the best player, but I enjoyed it as much as anyone. 

After college, I once again started playing bitcoin poker, but I decided to stop for a few reasons. I was a recreational player with limited knowledge of the game, and bitcoin prices were getting scary high. I became uncomfortable with the bitcoin stakes, and so I began to play on a site that used good old American dollars as its metric. This site also allowed something that the bitcoin site did not, a HUD display. A HUD display records all the actions you and your opponents make, and also tracks how much money you are earning or losing. I’m by no means a great poker player, but I enjoy it and would like to become a better player. I hope to use the HUD database to determine the expected outcome of any given poker hand.

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
From this data I hoped to build a model to predict the outcome of any given hand. The original 53 thousand rows contained cash hands as well as tournament hands. I won’t get into the differences here, but cash games are different from tournaments, so I elected to focus on the ~40k tournament hands at my disposal. Given the nature of my problem, there was little value in looking at the hands I didn’t play, as there was no outcome to train my model upon. I decided to look only at the hands where I wagered beyond what I was required to ante before any cards were dealt. This left me with a total of 10,695 hands, 20% of which was put into a holdout set. 

## Feature Creation
| buyin | BB_in_stack | players | position | low_card | high_card | suited | pocket_pair | card_rank |
|-------|-------------|---------|----------|----------|-----------|--------|-------------|-----------|
| 5.25  | 28.5        | 6       | 0.33     | 10       | 14        | 1      | 0           | 8         |
| 5.25  | 49.033      | 6       | 1        | 6        | 6         | 0      | 1           | 6         |
| 1.05  | 10.49       | 3       | 0.33     | 7        | 9         | 1      | 0           | 6.5       |
| 7.7   | 41.745      | 8       | 0.25     | 9        | 9         | 0      | 1           | 9         |
| 1.05  | 14.4        | 5       | 1        | 5        | 5         | 0      | 1           | 5         |
| 1.05  | 10.67       | 6       | 0.67     | 5        | 5         | 0      | 1           | 5         |

* Buy-in: the amount I paid to enter the tournament;

* Total-players: the number of players in the hand. These numbers range from 2-9;

* Position: this is my position at the table, as a fraction of the total players. In early position, you have to make your bet first, which generally puts you at a disadvantage to those who get to make their play after you. If I am in the dealer position, the latest possible position, the value for this feature is a 1. If I am in the small-blind, the earliest possible position, its value can be as low as 0.11; 

* Big Blinds in Stack: this is how much money I have, relative to the Big Blind. The Big Blind is the amount one player has to bet before any cards are dealt. It generally represents the minimum size of the bet as well. This ratio heavily dictates the strategy a poker player ought to follow in a tournament game;

* Suited: whether the two cards in my hand were of the same suit, represented by a boolean value of 1 for suited and 0 for unsuited. Having two cards of the same suit makes it easier to make flushes, one of the better possible Texas Hold’em hands;  

* Low Card: the lowest card in my hand, represented by an integer value. Values in this category range from 2, representing a 2, to 14, representing an ace; 

* High Card: the highest card in my hand, represented by an integer value, the same as “Low Card;”

* Card Rank: using a formula created by Bill Chen, a professional poker player with a degree in mathematics, I wanted to create a value to represent the strength of my hand. These values range from -1 for 7-2, the worst possible hand, to 20 for pocket aces, the strongest possible hand;


* Outcome Relative to Start & Made or Lost Money: Made or Lost Money was my target variable for Classification. It is a boolean value, with the positive class representing situations in which I made money or broke even and the negative class representing situations in which I lost money. It is fairly balanced in my dataset, with about 60% of values being in the positive class and 40% in the negative. 

![Amount Made](/images/won_lost_whole_df.png)

* Outcome relative to start was my target variable for regression. It is the amount I won or lost with respect to my starting stack, as a float. A value of 0 means I lost all my chips, and values between 0 and 1 mean I lost some of my starting chips. For example, if I had 100 chips, and this value is 0.95, that would mean I lost 5 chips. Values greater than 1 mean I made some amount of money. It's possible that these values could be as high as 9, but in practice are rarely higher than 2 or 3. When I switched to classification models, I converted it into a boolean, 0 for lost money, and 1 for made money or broke even. 

* Time Features: I elected not to use these, but they may be beneficial down the road. I created three different features:‘hour,’ ‘frequency,’ and ‘time_since_start’. ‘Hour’ was the hour of the day, ‘frequency’ was the number of hands I played in a 15 day period, and ‘time_since_start’ was the number of days that had gone by since I first started playing. 

## Expectations & Modeling Goals

It should be noted before I discuss modeling that there is a great deal of variance intrinsic to the game of poker. This is especially true of tournament poker, where often only 10-20% of the players walk away with cash in their pocket. Even very good tournament poker players will have long losing streaks. A simulation from Michael Acevedo’s book Modern Poker Theory found that over the course of 2000 tournaments a poker player with an average ROI of 25% can expect to lose as much as 8% of their original stake. 

This same sort of variation is present on a hand to hand basis as well. The best possible hand, pocket aces, will beat the worst hand 7-2 offsuit, around 87% of the time. This means that the question of whether I should play a poker hand is not the same as whether I will win a hand. Therefore my model can only hope to be a suggestion, and will not be able to perfectly predict whether I will make money or not. The plot below shows the hands I won versus the hands I lost with pocket aces. 

![Aces](/images/aces.png)

My modeling is only built from the hands that I did play. It is possible that there are lots of hands I ought to be playing that I am not, but I will not be able to answer this question unless I start playing all the hands I am dealt, which is certainly not an ideal strategy. There are many different ways to improve at poker, but my model hopes to answer one very specific and important question: given the manner in which I have historically played, will I most likely win money or lose money by playing any given poker hand given the conditions when cards are first dealt. 

## Regression Modeling

To determine which models would best predict the outcome of any given hand, I designed a function to run through 7 different possible models: Ridge, Lasso, KNN, Random Forest, AdaBoost, XGBoost, and Gradient Boost. I also wanted to see the predictive value of my time-related features for each of these various models, so I cycled through all possible combinations, as well as all possible exclusions. I used adjusted-R2 to measure the value of these features, and found that their inclusion generally reduced the predictive value of the models.

I used R2 as my metric to compare the different models. To my surprise, I found that Ridge and Lasso performed the best, followed by Gradient Boost. I started by tuning Ridge and Lasso, as well as Elastic Net, and found that Elastic Net regression performed the best, but not significantly better than it had with default parameters. I next turned to Gradient Boost. With parameter tuning I was able to get a gradient boost model which outperformed Ridge by about a factor of three. I built a composite model that used the predictions of Elastic Net as an additional predictive feature for Gradient Boost, but found this had little impact on the results. 

After running this model using cross validation, I found little improvement from the R2 value of Gradient Boost without the addition of Elastic Net. None of my R2 values for regression surpassed 0.015.


## Classification Modeling

It occurred to me that regression models were never going to be able to perform particularly well at the task I had given them. The amount someone wins or loses in poker is largely a product of the cards dealt to other players, the cards that hit the felt, as well as the strategies of other players. These were all things I had no way of feeding my model without supplying it with information that is unknown at the outset of a hand. At this junction I realized that I was approaching the problem in the wrong way. Rather than trying to predict how much I would win on any given hand, I elected to treat it as a classification problem. I decided to treat hands in which I made money or broke even as the positive class, and hands in which I lost money as the negative class. 

I started classification in a very similar manner to regression, looking at Brier scores as well as ROC AUC scores to get some idea of how the models were performing with default parameters. ROC AUC captures how often a model is making the correct prediction. A Brier score is a type of cost function for classification problems, and fulfills an analogous role to what mean squared error does for regression problems. Due to technical difficulties, I discluded Ridge and XGBoost, and added a simple logistic regression. I found that Gradient Boost performed the best across both metrics. AdaBoost performed 2nd best when looking at roc auc, while logistic performed 2nd best when looking at Brier. I decided to focus primarily on these three models. 

### Results of Testing
| model         | brier | roc_auc |
|---------------|-------|---------|
| GradientBoost | 0.226 | 0.641   |
| AdaBoost      | 0.249 | 0.637   |
| logistic      | 0.229 | 0.625   |
| RandomForest  | 0.249 | 0.597   |
| KNN           | 0.270 | 0.568   |

When I began tuning my models I decided to focus on the f1 score as the parameter to measure model performance, as it captured two things I was interested in. The first, precision, allowed me to know how much confidence I could put in a positive prediction. The second, recall, informed me of the opportunity cost of my model by factoring in the false positive rate. After tuning all my models I found that Gradient Boost performed the best with an f1 score of 0.75. Logistic and AdaBoost closely followed, with scores only a few percent worse than gradient boost. 

I tried to build a composite model as I did with my regression models. I evaluated the performance of these models by looking at several metrics. In poker there is a concept called ICM, and one of its principals is that your last chip is worth a lot more than your 1,000th chip. I therefore decided that it was important to minimize the rate of false positives, as these cases would lead me to losing money, making precision my most important metric. Essentially it allows me to know the stock I can put in a positive prediction by my model. 

I decided to also look at negative predictive value (NPV). It measures the rate of true negatives divided by the sum of true negatives and false negatives. By considering the NPV, I hoped to minimize the number of false positives, as these cases would lead to me missing out on hands that I was likely to win. For the reason stated above, however, I decided that it was secondary to precision. 

After performing 1000 cross validations on each model, I found the addition of my lesser models added little to no predictive value. I therefore decided to use gradient boost as my main model. 

Results
Using Gradient Boost with a threshold of 0.58 my model had a precision of about 0.675, an npv of 0.525, and an accuracy of 0.62. This meant that I could consider a positive prediction to be correct ~2/3  of the time, with a negative prediction being accurate slightly over half of the time. 

The model I created will hopefully push me in the direction of becoming a better poker player. I will put very little stock in a negative prediction, but I should very seriously consider any hands that it predicts I will win. While it is far from a perfect predictor, I can use it for situations where I feel that the expected value of playing a hand is close to that of folding it. In Data Science terms, I will continue to be the primary model making predictions at the poker table, but my Gradient Boosting model can serve as a secondary model that informs my decision making process. 

I also hope to be able to analyze Partial Dependence plots to help identify leaks in game. I am yet to do much serious analysis of these,  but one initial takeaway is that I tend to perform much worse when I have more big blinds in my stack. Given what I know about my playing style, this means I am probably playing too passively when this is the case. 

![Aces](/images/roc_curve.png)


## Next Steps
There are a number of avenues I could explore in order to expand upon the work done here. The first that comes to mind is looking at the situations in which my opponents showed their hands at the end of a round of poker. By doing this, I could look at how much equity I had in a hand, rather than just the net outcome after all the cards have hit the felt. My current target variable is partly a product of luck, while equity is not. At present the small sample size of such situations I have available to me makes this a troubling task. One solution might be to use the poker site I play on to try to get this data. After a certain amount of days they allow you to see what cards your opponent had. This would greatly increase the sample size available to me if I was able to combine that data with what I presently have. 

I could also attempt to insert time as a feature to see if my playing style has resulted in a higher rate of winning. Although I elected not to do it for the model I currently built, it may have greater utility with another type of modeling process.I may also attempt to create other features in my dataset. I would like to compute some statistics that capture some aspects of my opponents’ playing styles. 

Another avenue I hope to explore is post flop situations. This would mean working with a smaller dataset than I have presently, but I have already created features for much of this data. A model based upon this data would hopefully allow me to improve my strategy beyond the single decision my current model aims to inform. 
