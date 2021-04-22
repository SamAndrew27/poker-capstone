from sklearn.ensemble import GradientBoostingClassifier
from capstone3_data_prep import read_in_return_Xy_no_unused, read_in_return_Xy_scaled_no_unused
import pandas as pd 
import numpy as np 
from class_prep import threshold_testing, confusion, confusion_ratios


gb_final = GradientBoostingClassifier(learning_rate=.01, n_estimators=90, min_samples_leaf=6 , min_samples_split=4 ,max_features= 3,max_depth= 5,subsample= .6)


X, y = read_in_return_Xy_no_unused()





if __name__=="__main__":

    thresholds = [.5,.51,.52,.53,.54,.55,.56,.57,.58,.59,.6,.61,.62,.63,.64,.65,.66,.67]

    # print(threshold_testing(X,y,gb_final, thresholds))
    #    thresh        f1  accuracy precision    recall
    # 0     0.5  0.761121  0.645512  0.637658  0.944031
    # 1    0.51  0.761108  0.649369  0.642448  0.933603
    # 2    0.52  0.757732  0.649838  0.646678  0.915687
    # 3    0.53  0.757227  0.654511  0.653304  0.900583
    # 4    0.54  0.753532  0.657437  0.661757   0.87591
    # 5    0.55  0.748956  0.659071  0.669358  0.850221
    # 6    0.56  0.748318  0.666786  0.682832  0.828662
    # 7    0.57  0.740537  0.667602  0.694593  0.793347
    # 8    0.58   0.72442  0.657665  0.698846   0.75282
    # 9    0.59  0.700385  0.645864  0.709397  0.692694
    # 10    0.6  0.679033  0.637566  0.722905  0.641611
    # 11   0.61  0.653304  0.626111  0.733337   0.58965
    # 12   0.62  0.621514  0.609398  0.739189  0.536491
    # 13   0.63  0.593634  0.597243  0.749342  0.492053
    # 14   0.64  0.554329  0.579358  0.757746  0.438632
    # 15   0.65  0.508505  0.561829  0.773079  0.379616
    # 16   0.66  0.438114  0.534597  0.788436  0.303896
    # 17   0.67  0.365839  0.509467  0.807476   0.23677
    thresh = .59
    print(confusion_ratios(X,y,gb_final, thresh, 10))
    print(confusion(X,y,gb_final, thresh))