import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
import numpy as np 
from sklearn.inspection import plot_partial_dependence
import matplotlib.pyplot as plt 

# returns X and y with 

def grid_search(X, y, model, param_grid, return_stuff = False):
    
    gscv = GridSearchCV(estimator= model, param_grid=param_grid, n_jobs = -1, verbose=1, scoring='r2')

    gscv.fit(X, y)

    print(gscv.best_estimator_)
    print(gscv.best_score_)   

    if return_stuff:
        return gscv.best_estimator_, gscv.best_score_

# produces X_train, X_test, y_train, y_test with relevant columns
def read_in_and_split():
    df = pd.read_csv('/home/sam/Documents/DSI/capstone/poker/data/train_tournaments.csv')
    X = df[['buyin', 'total_players', 'position', 'BB_in_stack',
        'suited',  'low_card','high_card','card_rank','hour',
        'days_since_start', 'hand_frequency', 'outcome_relative_to_start']]

    y = X['outcome_relative_to_start']
    del X['outcome_relative_to_start']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .2, random_state=127)

    return X_train, X_test, y_train, y_test 

# returns just X and y, no test 
def read_in_return_Xy():
    df = pd.read_csv('/home/sam/Documents/DSI/capstone/poker/data/train_tournaments.csv')
    X = df[['buyin', 'total_players', 'position','BB_in_stack', 
        'suited',  'low_card','high_card','card_rank','hour',
        'days_since_start', 'hand_frequency', 'outcome_relative_to_start']]

    y = X['outcome_relative_to_start']
    del X['outcome_relative_to_start']

    return X, y 

def read_in_return_Xy_no_time():
    df = pd.read_csv('/home/sam/Documents/DSI/capstone/poker/data/train_tournaments.csv')
    X = df[['buyin', 'total_players', 'position','BB_in_stack', 
        'suited',  'low_card','high_card','card_rank', 'outcome_relative_to_start']]

    y = X['outcome_relative_to_start']
    del X['outcome_relative_to_start']

    return X, y 
# returns X and y, X scaled, y w/ log transform 
# doesn't include any time data 
def scaled_and_logged_X_y():
    X, y = read_in_return_Xy()
    SS = StandardScaler()
    X = X[['buyin', 'BB_in_stack', 'total_players', 'position', 'suited',  'low_card','high_card','card_rank']]
    X_total_cols = list(X.columns)
    X = pd.DataFrame(data = SS.fit_transform(X), columns = X_total_cols)
    y = y.apply(lambda x: np.log(x + 1))
    return X, y 

# returns X and y logged
# doesn't include any time data
def X_and_logged_y():

    X, y = read_in_return_Xy()

    X = X[['buyin', 'BB_in_stack', 'total_players', 'position', 'suited',  'low_card','high_card','card_rank']]

    y = y.apply(lambda x: np.log(x + 1))
    return X, y

def partial_plot(X,y,model, feature_to_plot = 0):
    fig, ax = plt.subplots()
    model.fit(X,y)
    ppd = plot_partial_dependence(model, X,[feature_to_plot], ax=ax)# will change this to a return statement once i'm ready to start saving plots
    
    plt.show()

def partial_plot_multiple(X,y,model, features_to_plot):
    fig, ax = plt.subplots()
    model.fit(X,y)
    ppd = plot_partial_dependence(model, X,[features_to_plot], ax=ax)
    
    plt.show() # will change this to a return statement once i'm ready to start saving plots

