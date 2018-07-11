import pandas as pd
from Packages.Data import helper as data_helper

#SQL connection
engine,conn = data_helper.instantiate_engine()
coin_df = pd.read_csv('coins.csv')
#loop through coins
#find the gaps in data
# for coin in coin_df.values:
#     coin = coin[0]
coin = 'LTC'
print('Working on {}'.format(coin))
market = '{}BTC'.format(coin)
stmt = '''SELECT open_time from {}_binance_raw ORDER BY open_time DESC'''.format(coin)
df = pd.read_sql(stmt, conn)
df['diff'] = df.open_time - df.open_time.shift(-1)
df['prev'] = df.open_time.shift(-1)
df.prev += 60000
temp_df = df.loc[df['diff'] > 60000].copy()
out_df = temp_df[['open_time', 'prev']].copy()
out_df.dropna(inplace=True)
out_df.rename(columns={'open_time':'end', 'prev':'start'},inplace=True)
out_df['start'] = out_df['start'].astype(int)
out_df['end'] = out_df['end'].astype(int)
out_df.to_csv('missing_epochs/{}.csv'.format(coin),index=None)