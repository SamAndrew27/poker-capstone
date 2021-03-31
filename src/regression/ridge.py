from sklearn.linear_model import Ridge 
from regression_prep import scaled_and_logged_X_y, grid_search



X, y = scaled_and_logged_X_y()
rg = Ridge()


# Ridge(alpha=450, solver='sag')
# 0.0042368637340820525
# both sag and saga seem to be optimal
# alpha values of around 400-450

if __name__ == "__main__":

    param_grid = {'alpha': [.01,.05, .1,.2,.3,.4,.5,.6,.7,.8,.9,1,5,10,20,50,100,200, 300, 350, 375, 400, 425, 450, 475, 500, 600, 700, 800, 825, 850, 875, 900, 925, 950, 975, 1000], # consider looking at learning_rate, loss, 
            'solver': ['sparse_cg', 'sag', 'saga']}
    grid_search(X, y, rg, param_grid)