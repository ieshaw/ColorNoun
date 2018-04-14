__author__ = 'Ian'

import os
import pandas as pd


raw_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '/CSVs/Raw/Hourly/'

out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '/CSVs/Processed/Hourly/'

i = 0

for file in os.listdir(raw_dir):

    coin = file.split('-')[0]

    coin_df = pd.read_csv(raw_dir + file)

    coin_df.index = coin_df['time']

    x_df = pd.DataFrame(index= coin_df['time'])

    x_df['spread_{}'.format(coin)] = coin_df['high'] - coin_df['low']

    x_df[['volumefrom_{}'.format(coin) ,'volumeto_{}'.format(coin)]] = coin_df[['volumefrom' ,'volumeto']]

    #normalize

    normal_len = 5

    # normal_len = 24 * 30

    x_df = (x_df - x_df.rolling(window= normal_len, min_periods= normal_len).mean())\
           /x_df.rolling(window=normal_len, min_periods=normal_len).std()

    ret_df = coin_df['open'].pct_change()

    #shift so the return information over a time period is associate diwht the spread and volume of that time period

    ret_df = ret_df.shift(-1)

    x_df['return_{}'.format(coin)] = ret_df

    x_df = x_df.dropna()

    y_df = pd.DataFrame(index=x_df.index)

    y_df['return_{}'.format(coin)] = ret_df.shift(-1).loc[y_df.index]

    if i == 0:

        X_df = x_df

        Y_df = y_df

        i = 1

    else:

        X_df = X_df.join(x_df, how = 'inner')

        Y_df = Y_df.join(y_df, how = 'inner')

X_df.to_csv(out_dir + 'X.csv')
Y_df.to_csv(out_dir + 'Y.csv')



