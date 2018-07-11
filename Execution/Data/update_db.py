import pandas as pd
import Packages.Data.helper as data_helper
from Packages.API.General.helper import key_retriever,instantiate_api_object

#Use binance account to pull data
key_path = '.exchange_keys.json'
key_name = 'Binance_Alpha'
key_status = 'ro'
exchange, public_key, private_key = key_retriever(key_path,key_name,key_status)
api_object = instantiate_api_object(exchange, public_key, private_key)
engine,conn = data_helper.instantiate_engine()
ex_info_df = pd.DataFrame(api_object.get_exchange_info()['symbols'])
ex_info_df = ex_info_df.loc[ex_info_df.quoteAsset == 'BTC']
num_coins = len(ex_info_df)
print('{} Currencies to update.'.format(num_coins))
i = 1
for index,row in ex_info_df.iterrows():
    coin = row.baseAsset
    #only update in the VAR list
    if coin in ['ADA', 'NEBL', 'BCPT', 'NEO', 'FUN']:
        market = row.symbol
        print('Uploading: {}. Currency {} of {}'.format(coin, i, num_coins))
        last_epoch = data_helper.get_last_epoch_binance_raw_data(coin=coin, conn=conn)
        klines = api_object.get_historical_klines(market, '1m', start_str=str(last_epoch))
        df = pd.DataFrame(klines, columns=['open_time', 'open', 'high', 'low', 'close', 'volume',
                                           'close_time', 'quote_asset_volume', 'num_trades', 'taker_buy_base_asset_volume',
                                           'taker_buy_quote_asset_volume', 'ignore'])
        df['coin'] = coin
        df = df.loc[df.open_time > last_epoch].copy()
        table_name = '{}_binance_raw'.format(coin)
        data_helper.upload_df_to_db(df, table_name, engine)
        i += 1