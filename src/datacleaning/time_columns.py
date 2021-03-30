import pandas as pd 
import numpy as np 
from datetime import timedelta

def fill_time_columns(df):

    df['HandHistoryTimestamp'] = df['HandHistoryTimestamp'].apply(lambda x: pd.to_datetime(x) - timedelta(hours=6)) # remove 6 hours from timestamp to get it into mountain time 

    df['hour'] = df['HandHistoryTimestamp'].apply(lambda x: x.hour) # will need to determine degree to which time is offset

    df['year_month_day'] = pd.to_datetime(df['HandHistoryTimestamp']).dt.to_period('D').dt.to_timestamp()  # will need to determine degree to which time is offset

    df['days_since_start'] = df['year_month_day'].apply(lambda x: (x - pd.to_datetime('2019-10-23 00:00:00')).days)

    f_dic = frequency_dict(df)

    df['hand_frequency'] = df['days_since_start'].apply(lambda x: hand_frequency(x, f_dic))

    return df


###########################################################################################


def hand_frequency(x, dic): # uses dictionary created from above to assign a value to each row 
    return dic[x]



def frequency_dict(df): # hands played in 15 day period (7 days before, current day, 7 days after)
    result = {}
    date_range = np.array([-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7]) # maybe change this to an argument 
    last_day = df['days_since_start'].iloc[-1] # get last day's day number
    day = 0
    while date_range[7] <= last_day: 
        day_count = 0 # counts number of hands for that given hands day range

        for num in date_range:
            mask = df['days_since_start'] == num
            day_count += df[mask].shape[0]
        result[day] = day_count
        day += 1
        date_range +=1
    return result