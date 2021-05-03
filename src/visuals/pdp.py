from sklearn.ensemble import GradientBoostingClassifier
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.inspection import plot_partial_dependence
from load_df import join_training_holdout
# plt.style.use('ggplot')

model = GradientBoostingClassifier(learning_rate=.01, n_estimators=90, min_samples_leaf=6 , min_samples_split=4 ,max_features= 3,max_depth= 5,subsample= .6)


X, y = join_training_holdout(target=True)
X.columns = ['Suited', # 0
             'Low Card', # 1
             'Position', # 2
             'High Card', # 3 
             'Card Rank', # 4
             'Limpers', # 5
             'Raises & Re-Raises', # 6 
             '# of Players to Enter Pot', # 7 
             'Number of Players Yet to Act', # 8
             'BBs in Stack'] # 9 


def partial_plot(X, y, model, feature_to_plot, title = 'Default', save=False, plot_file='Default'):
    """creates pdp plot for a single feature

    Args:
        X (array): features
        y (array): targets
        model: sklearn model to be used
        feature_to_plot (int): feature to plot (see columns of X to determine number)
        title (str, optional): title used in plot. Defaults to 'Default'.
        save (bool, optional): Whether to save the plot. If False plot is displayed rather than saved. Defaults to False.
        plot_file (str, optional): name of file. Defaults to 'Default'. Only applicable if 'save' is set to True
    """    
    model.fit(X, y)

    fig, ax = plt.subplots(figsize=(12,12))

    display  = plot_partial_dependence(model, X, [feature_to_plot], ax=ax)
    plt.title(title)
    plt.tight_layout()
    if save:
        plt.savefig(f'../../images/feature_importances/{plot_file}.png', dpi=fig.dpi)
    else:
        plt.show()

def partial_plot_multiple(X, y, model, features_to_plot, title='Default', save=False, plot_file = 'Default'):
    """creates pdp plot for 2 features

    Args:
        X (array): features
        y (array): targets
        model: sklearn model to be used
        feature_to_plots (list): features to plot (see columns of X to determine number)
        title (str, optional): title used in plot. Defaults to 'Default'.
        save (bool, optional): Whether to save the plot. If False plot is displayed rather than saved. Defaults to False.
        plot_file (str, optional): name of file. Defaults to 'Default'. Only applicable if 'save' is set to True
    """    
    model.fit(X, y)

    fig, ax = plt.subplots(figsize=(12,12))

    display = plot_partial_dependence(model, X, [features_to_plot], ax=ax)# takes list of 2 features to plot
    plt.title(title)
    if save:
        plt.savefig(f'../../images/feature_importances/{plot_file}.png',  dpi=fig.dpi)
    else:
        plt.show()    


if __name__ == "__main__":
    plt.rcParams.update({'font.size': 25})

    # print(partial_plot(X, y, grad_boost, title = 'Position', feature_to_plot=3))
    # partial_plot_multiple(X, y, grad_boost, features_to_plot=[5,4], title='High/Low Card')

    title = 'Number Players Before / After\nPartial Dependence Plot'
    # feature = 9
    features_to_plot = [6,5]
    plot_file = 'num_before_after2'

    partial_plot_multiple(X,y,model,features_to_plot=features_to_plot, title=title)
    # partial_plot_multiple(X,y,model,features_to_plot = features_to_plot, title=title, save=True, plot_file=plot_file)

    # partial_plot(X, y, model, feature, title=title)
    # partial_plot(X, y, model, feature, title=title, save=True, plot_file=plot_file)

    # 'Suited', # 0
    # 'Low Card', # 1
    # 'Position', # 2
    # 'High Card', # 3 
    # 'Card Rank', # 4
    # 'Limpers', # 5
    # 'Raises & Re-Raises', # 6 
    # '# of Players to Enter Pot', # 7 
    # 'Number of Players Yet to Act', # 8
    # 'BBs in Stack'] # 9 