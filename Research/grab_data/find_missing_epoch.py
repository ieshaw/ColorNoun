import pandas as pd
import helper as data_helper
from Packages.API.General.helper import key_retriever,instantiate_api_object

key_path = '.exchange_keys.json'
key_name = 'Binance_Alpha'
key_status = 'ro'
exchange, public_key, private_key = key_retriever(key_path,key_name,key_status)
api_object = instantiate_api_object(exchange, public_key, private_key)
engine,conn = data_helper.instantiate_engine()
#set the coin and market
coin = 'NEO'
market = 'NEOBTC'

#find the gaps in data
stmt = '''SELECT open_time from binance_historic_data_raw 
WHERE coin='{}' ORDER BY open_time DESC'''.format(coin)
df = data_helper.query_db(stmt, conn)
df['diff'] = df.open_time - df.open_time.shift(-1)
df['prev'] = df.open_time.shift(-1)
df.prev += 60000
missing_data = df.loc[df['diff'] > 60000].copy()
missing_tuples = list(zip(missing_data.prev.astype(int), missing_data.open_time.astype(int)))
#grab that data
this_tuple = missing_tuples[1]
start_epoch = this_tuple[0]
end_epoch = this_tuple[1]
klines = api_object.get_historical_klines(market, '1m', start_str=str(start_epoch),
                                          end_str=str(end_epoch))
df = pd.DataFrame(klines, columns=['open_time', 'open', 'high', 'low', 'close', 'volume',
                                   'close_time', 'quote_asset_volume', 'num_trades', 'taker_buy_base_asset_volume',
                                   'taker_buy_quote_asset_volume', 'ignore'])
print('Requested Start Epoch: {}'.format(start_epoch))
print('Requested End Epoch: {}'.format(end_epoch))
print('Data Start Epoch: {}'.format(df.open_time.max()))
print('Data End Epoch: {}'.format(df.open_time.min()))