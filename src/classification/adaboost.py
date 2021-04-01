import pandas as pd
from class_prep import read_in_return_Xy_no_time, grid_search
from sklearn.ensemble import AdaBoostClassifier

X, y = read_in_return_Xy_no_time()

ada = AdaBoostClassifier()

    # AdaBoostClassifier(learning_rate=0.02, n_estimators=120)
    # 0.7485170094269646
    # AdaBoostClassifier(learning_rate=0.021, n_estimators=119)
    # 0.7485720012874677


if __name__ == "__main__":
    param_grid = {'learning_rate': [.201,.202,.203,.204, .0205,.206,.207,.208,.209,.021,.211,.212,.213,.214,.0215,.0216,.217,.218,.219],
            'n_estimators': [119]}

    grid_search(X, y, ada, param_grid)