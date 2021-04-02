from sklearn.ensemble import GradientBoostingClassifier
import matplotlib.pyplot as plt
import pandas as pd
from class_prep import read_in_return_Xy_no_time
from sklearn.inspection import plot_partial_dependence

grad_boost = GradientBoostingClassifier(learning_rate=.042, max_depth=2, max_features=2,
                                        min_samples_leaf=9, min_samples_split=6, n_estimators=37, subsample=.3)

X, y = read_in_return_Xy_no_time()


def partial_plot(X, y, model, feature_to_plot, title, show=True, plot_file=None):
    model.fit(X, y)

    fig, ax = plt.subplots(figsize=(12,12))

    display  = plot_partial_dependence(model, X, [feature_to_plot], ax=ax)
    plt.title(title)
    if show:
        plt.show()
    else:
        plt.savefig(plot_file, dpi=fig.dpi)

def partial_plot_multiple(X, y, model, features_to_plot, title, show=True, plot_file = None):
    model.fit(X, y)

    fig, ax = plt.subplots(figsize=(12,12))

    display = plot_partial_dependence(model, X, [features_to_plot], ax=ax)# takes list of 2 features to plot
    plt.title(title)
    if show:
        plt.show()    
    else:
        plt.savefig(plot_file,  dpi=fig.dpi)


if __name__ == "__main__":
    plt.rcParams.update({'font.size': 25})
    print(X.info())
    print(partial_plot(X, y, grad_boost, title = 'Position', feature_to_plot=3))
    # partial_plot_multiple(X, y, grad_boost, features_to_plot=[5,4], title='High/Low Card', show=False, plot_file='high_low.png')
    # print(X.info())