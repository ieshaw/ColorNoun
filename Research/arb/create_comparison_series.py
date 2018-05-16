import pandas as pd
import time

bin_df = pd.read_csv('bin.csv')
bit_df = pd.read_csv('bit.csv')

print(bin_df.shape)
print(bit_df.shape)
#make sure only to save the time we a# lso have binance data for
bit_df = bit_df.T.apply(lambda x: int(time.mktime(time.strptime(x.values[0], '%Y-%m-%dT%H:%M:%S'))))
print(bit_df.type)
print(bit_df.head())
# bit_df = bit_df.loc[bit_df.T.isin(time_epochs)].copy()
# print(bit_df)
# bit_df.to_csv('bit.csv', index=False)