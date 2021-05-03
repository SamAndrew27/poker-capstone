import numpy as np
import pandas as pd
import pickle 
from sklearn.ensemble import GradientBoostingClassifier

from data_prep import training_data_Xy, read_in_holdout_Xy, get_data_and_join



def pickle_model(name='model'):
    """Pickles model for use in flask app

    Args:
        name (str, optional): name of file to save model to. Defaults to 'model'.
    """    
    gb_final = GradientBoostingClassifier(learning_rate=.01, n_estimators=90, min_samples_leaf=6 , min_samples_split=4 ,max_features= 3,max_depth= 5,subsample= .6)
    X,y = get_data_and_join()
    gb_final.fit(X,y)
    pickle.dump(gb_final, open(f'../../flask/flask_AB/models/{name}.pickle', 'wb'))
    pickle.dump(gb_final, open(f'../../flask/flask_standard/models/{name}.pickle', 'wb'))



if __name__=='__main__':
    # X, y = get_data_and_join()
    # print(X.info())
    pickle_model('final_model')