import numpy as np
import pandas as pd
import time
from Packages.API.General.helper import key_retriever, instantiate_api_object, get_exchange_df
from Packages.API.Bittrex_Helper.helper import instantiate_api_object as bit_iao

key_path = '.exchange_keys.json'
key_status = 'ro'
#create api objects
exchange ,public_key, private_key = key_retriever(key_path, 'Binance_Alpha', status='ro')
bin_api = instantiate_api_object(exchange,public_key,private_key)
exchange ,public_key, private_key = key_retriever(key_path, 'Bittrex_Alpha', status='ro')
bit1 = bit_iao(public_key, private_key, api_version='v1.1')
bit2 = bit_iao(public_key, private_key, api_version='v2.0')
#decide on which tickers to grab
bit_ticks = get_exchange_df('Bittrex', bit1)
bin_ticks = get_exchange_df('Binance', bin_api)
inner_ticks = bit_ticks.join(bin_ticks, how='inner', lsuffix='_bit', rsuffix='_bin')
inner_ticks = inner_ticks.loc[inner_ticks.index != 'BTC'].copy()
#grab the binance recent data
i = 0
for index, row in inner_ticks.iterrows():
    market = row.market_bin
    bin_data = pd.DataFrame(bin_api.get_historical_klines(symbol=market, interval='1m', start_str="200 hours ago UTC"))
    #only look at open prices
    new_df = bin_data[[0, 1]].copy()
    new_df.rename({0: 'T', 1: index}, axis='columns', inplace=True)
    if i == 0:
        bin_df = new_df
        i = 1
    else:
        bin_df = bin_df.merge(new_df, how='inner', on='T')
bin_df.to_csv('bin.csv', index=False)
#grab the bittrex recent data
i = 0
for index, row in inner_ticks.iterrows():
    market = row.market_bit
    #bittrex api unreliable skip if can't get response
    try:
        bit_data = pd.DataFrame(bit2.get_candles(market=market, tick_interval='oneMin')['result'])
        # only look at open prices
        bit_data[index] = bit_data.O
    except Exception as e:
        print(index, e)
        continue
    new_df = bit_data[['T', index]]
    print(new_df.head())
    if i == 0:
        bit_df = new_df
        i = 1
    else:
        bit_df = bit_df.merge(new_df, how='outer', on='T')
bit_df.to_csv('bit.csv', index=False)