import pandas as pd 
from sklearn.preprocessing import StandardScaler

def read_in_data():
    df = pd.read_csv('/home/sam/Documents/DSI/capstone/poker/data/train_classification_tournaments.csv')
    df = df.drop(df.columns[0], axis = 1)

    return df

def read_in_return_Xy():
    X = read_in_data()


    y = X['made_or_lost']
    del X['made_or_lost']

    return X, y 

def read_in_return_Xy_no_time():
    X = read_in_data()
    y = X['made_or_lost']

    X =  X.drop(['made_or_lost', 'hour', 'days_since_start', 'hand_frequency'], axis = 1)

    return X, y 

def read_in_return_X_scaled():
    X = read_in_data()
    y = X['made_or_lost']
    del X['made_or_lost']

    SS = StandardScaler()
    X = pd.DataFrame(data = SS.fit_transform(X), columns = list(X.columns))    

    return X, y

def read_in_return_X_scaled_no_time():
    X = read_in_data()
    y = X['made_or_lost']
    X =  X.drop(['made_or_lost', 'hour', 'days_since_start', 'hand_frequency'], axis = 1)

    SS = StandardScaler()
    X = pd.DataFrame(data = SS.fit_transform(X), columns = list(X.columns))    

    return X, y



if __name__ == "__main__":
    X, y = read_in_return_X_scaled()
    print(y)