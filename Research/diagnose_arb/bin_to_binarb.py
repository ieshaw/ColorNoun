import pandas as pd
import numpy as np
'''
goal is to take the bit.csv and turn it into bitarb.csv with columns
market, time(UTC), price, side(sell or buy),quantity
'''

bin_df = pd.read_csv('bin.csv')
out_df = pd.DataFrame()
out_df[['market','time','side','price','quantity']] = bin_df[['market','time','isBuyer','price','qty']]
out_df.side = out_df.side.map({True:1,False:-1})
out_df.to_csv('binarb.csv',index=False)
