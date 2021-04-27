from sklearn.linear_model import Lasso 
from regression_prep import grid_search, scaled_and_logged_X_y

X, y = scaled_and_logged_X_y()
las = Lasso()

# performs the worst out of ridge and elastic
# likes a very low alpha of .05
# seems to prefer cyclic

if __name__ == "__main__":
    param_grid = {'alpha': [.05, .1, .15, .2, .3, .4, .5, .6, .7, .8, .9, 1, 4, 10, 20, 50, 400, 450], # consider looking at learning_rate, loss, 
                  'selection': ['cyclic', 'random']}
    grid_search(X, y, las, param_grid)
