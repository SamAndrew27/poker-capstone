from sklearn.linear_model import ElasticNet
from regression_prep import scaled_and_logged_X_y, grid_search


X, y = scaled_and_logged_X_y()
EN = ElasticNet()
 

    # random doesn't seem to matter much
    # ElasticNet(alpha=0.05, l1_ratio=0.0105, selection='random')
    # 0.004164399644645855

if __name__ == "__main__":

    param_grid = {'alpha': [.05, .1, .15, .2, .3, .4, .5, 1, 4, 10, 20, 50, 400, 450], # consider looking at learning_rate, loss, 
                'l1_ratio': [.0105, .011, .0115, .012, .013, .014, .015, .0155, .016, .0165, .017, .018, .019, .02, .03, .04, .05, .06, .07, .08, .09, .1],
                'selection': ['cyclic', 'random']}
    
    grid_search(X, y, EN, param_grid)