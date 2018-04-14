__author__ = 'Ian'

import requests
import datetime
import os
import pandas as pd


coins = ['ETH', 'XRP','LTC', 'DASH', 'XMR']

for coin in coins:

    url = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '/Polo_Jsons/{}.json'.format(coin)
    compare_coin = 'BTC'
    df = df = pd.read_json(url)
    df.to_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '/CSVs/Raw/Polo/{}-{}.csv'.format(coin, compare_coin), index= False)

    print(df.shape)