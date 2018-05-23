import pandas as pd
import helper as data_helper

engine,conn = data_helper.instantiate_engine()
# stmt = '''SELECT DISTINCT coin from binance_historic_data_raw'''
# df = data_helper.query_db(stmt, conn)
# df.to_csv('coins.csv', index=None)
coin_df = pd.read_csv('coins.csv')
#loop through coins
#find the gaps in data
for coin in coin_df.values:
    coin = coin[0]
    stmt = '''SELECT open_time from binance_historic_data_raw
    WHERE coin='{}' ORDER BY open_time DESC'''.format(coin)
    df = data_helper.query_db(stmt, conn)
    df['diff'] = df.open_time - df.open_time.shift(-1)
    df['prev'] = df.open_time.shift(-1)
    df.prev += 60000
    missing_data = df.loc[df['diff'] > 60000].copy()
    missing_tuples = list(zip(missing_data.prev.astype(int), missing_data.open_time.astype(int)))
    print(coin, missing_tuples)