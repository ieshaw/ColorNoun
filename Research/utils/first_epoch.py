import pandas as pd
from Packages.Data import helper as data_helper

engine,conn = data_helper.instantiate_engine()
coin_df = pd.read_csv('coins.csv')
out_list = []
for coin in coin_df.values:
    coin = coin[0]
    stmt = '''SELECT open_time from {}_binance_raw ORDER BY open_time ASC LIMIT 1'''.format(
        coin)
    df = pd.read_sql(stmt, conn)
    epoch = df.values[0][0]
    out_list.append({'coin':coin,'first_epoch':epoch})
pd.DataFrame(out_list).to_csv('first_epoch.csv', index=False)