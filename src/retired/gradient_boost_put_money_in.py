from regression_prep import first_regression_df, second_regression_df, third_regression_df
import pandas as pd
import numpy as np 
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.inspection import plot_partial_dependence
import matplotlib.pyplot as plt 



X, y = third_regression_df()



def gbr_cv(X, y, lr = .05, n_est = 100, mf = 2, md = 2, msl = 8, mss = 4):
    gbr = GradientBoostingRegressor(learning_rate= lr, n_estimators=n_est, max_depth= md, max_features= mf, min_samples_leaf=msl, min_samples_split=mss)
    r2_score = cross_val_score(gbr, X, y, n_jobs = -1, scoring= 'r2')
    mse = cross_val_score(gbr, X, y, n_jobs = -1, scoring= 'neg_mean_squared_error')

    return f'R2: {np.mean(r2_score)} - MSE: {-np.mean(mse)}' 




def grid_search_gbr(X, y, param_grid = None):
    gbr = GradientBoostingRegressor()
    if param_grid == None:
        param_grid = {'min_samples_split': [2,3,4,6], # consider looking at learning_rate, loss, 
                    'max_features': [3,4,5,6,7],
                    'max_depth': [2,3,4, 5,6],
                    'min_samples_leaf': [1, 2,4,8]}
    
    gbr_gscv = GridSearchCV(estimator= gbr, param_grid=param_grid, n_jobs = -1, verbose=1, scoring='r2')

    gbr_gscv.fit(X, y)

    print(gbr_gscv.best_estimator_)
    print(gbr_gscv.best_score_)   



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

if __name__ == "__main__":

    print(X.info())
    # gradient_regressor = GradientBoostingRegressor(learning_rate=.1, max_features=3, max_depth=2,min_samples_leaf=2,min_samples_split=4)   
    # gradient_regressor.fit(X,y)


    
    '''
    results using third regression of gridsearch
    GradientBoostingRegressor(max_depth=2, max_features=3, min_samples_leaf=8)
    0.0022602506949171764
    '''
    model3 = GradientBoostingRegressor(max_depth=2, max_features=3, min_samples_leaf=8)

    model3.fit(X,y)

    print(model3.feature_importances_)



    # partial_plot_multiple(X,y,model3, [3,6])

    partial_plot(X, y, model3, 2)