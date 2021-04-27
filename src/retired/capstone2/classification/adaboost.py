import pandas as pd
from class_prep import read_in_return_Xy_no_time, grid_search, threshold_testing, confusion
from sklearn.ensemble import AdaBoostClassifier

X, y = read_in_return_Xy_no_time()

ada = AdaBoostClassifier()

    # AdaBoostClassifier(learning_rate=0.02, n_estimators=120)
    # 0.7485170094269646
    # AdaBoostClassifier(learning_rate=0.021, n_estimators=119)
    # 0.7485720012874677

ada_final = AdaBoostClassifier(learning_rate=.021, n_estimators= 119)


if __name__ == "__main__":
    param_grid = {'learning_rate': [.201,.202,.203,.204, .0205,.206,.207,.208,.209,.021,.211,.212,.213,.214,.0215,.0216,.217,.218,.219],
            'n_estimators': [119]}

    #grid_search(X, y, ada, param_grid)
    # threshes = [.1,.15,.2,.25,.3,.45,.5]
    threshes = [.505,.51, .515,.52,.525,.53, .535, .54]
    # print(threshold_testing(X, y, ada_final, threshes).sort_values('f1', ascending=False))

    print(confusion(X,y,ada_final,.52))


    #   thresh         f1  accuracy precision     recall
    # 0    0.5   0.747677  0.599695  0.599931   0.992673
    # 1   0.51   0.722406  0.621784   0.64413    0.82438
    # 2   0.52   0.706708  0.624243  0.662265   0.757745
    # 3   0.53   0.662256  0.607525  0.681328   0.644649
    # 4   0.54   0.611087  0.585671  0.695326   0.545937
    # 5   0.55   0.530872  0.553415  0.714134   0.423384
    # 6   0.56   0.455709  0.525715   0.72584   0.332811
    # 7   0.57    0.17291  0.443316  0.772213  0.0977712
    # 8   0.58   0.106501  0.427186  0.788665  0.0572371
    # 9   0.59  0.0764216  0.420642  0.825983  0.0402965

    #   thresh        f1  accuracy precision    recall
    # 0  0.505  0.734413  0.621668  0.633275  0.875399
    # 1   0.51  0.724422  0.624243  0.644889  0.826882
    # 2  0.515    0.7159  0.622486  0.650885  0.796161
    # 3   0.52  0.705448  0.620384  0.658296  0.761306
    # 4  0.525  0.683115  0.611148  0.666236  0.703009
    # 5   0.53   0.66406  0.607995  0.680771  0.648312
    # 6  0.535  0.648234  0.601332  0.685243  0.615695
    # 7   0.54  0.617037  0.588011  0.693905  0.555835
