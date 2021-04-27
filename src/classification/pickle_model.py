from sklearn.ensemble import GradientBoostingClassifier
import pandas as pd
import numpy as np
import pickle 
from data_prep import training_data_Xy, read_in_holdout_Xy

def get_data_and_join():
    X_training, y_training = training_data_Xy()
    X_hold, y_hold = read_in_holdout_Xy()

    X_training['made_or_lost'] = y_training
    X_hold['made_or_lost'] = y_hold
    all_data = pd.concat([X_training, X_hold], ignore_index=True)

    y = all_data['made_or_lost']
    X = all_data.drop(['made_or_lost'], axis=1)

    return X, y 

def pickle_model(name='model'):
    gb_final = GradientBoostingClassifier(learning_rate=.01, n_estimators=90, min_samples_leaf=6 , min_samples_split=4 ,max_features= 3,max_depth= 5,subsample= .6)
    X,y = get_data_and_join()
    gb_final.fit(X,y)
    pickle.dump(gb_final, open(f'../../flask/models/{name}.pickle', 'wb'))



if __name__=='__main__':
    # X, y = get_data_and_join()
    # print(X.info())
    pickle_model('final_model')