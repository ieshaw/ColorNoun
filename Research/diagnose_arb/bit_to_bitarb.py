import pandas as pd
import numpy as np
'''
goal is to take the bit.csv and turn it into bitarb.csv with columns
market, time(UTC), price, side(sell or buy),quantity
'''

bit_df = pd.read_csv('bit.csv')
out_df = pd.DataFrame()
out_df[['market','time','side','price','quantity']] = bit_df[['Exchange','Closed','OrderType','PricePerUnit','Quantity']]
out_df.time = pd.DatetimeIndex(out_df.time).view('int64')// pd.Timedelta(1, unit='s')
out_df.side = out_df.side.map({'LIMIT_SELL':-1, 'LIMIT_BUY':1})
out_df.to_csv('bitarb.csv', index=False)