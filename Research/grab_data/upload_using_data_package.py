import pandas as pd
import helper as data_helper
from Packages.API.General.helper import key_retriever,instantiate_api_object

key_path = '.exchange_keys.json'
key_name = 'Binance_Alpha'
key_status = 'ro'

exchange, public_key, private_key = key_retriever(key_path,key_name,key_status)
api_object = instantiate_api_object(exchange, public_key, private_key)
engine,conn = data_helper.instantiate_engine()
ex_info_df = pd.DataFrame(api_object.get_exchange_info()['symbols'])
ex_info_df = ex_info_df.loc[ex_info_df.quoteAsset == 'BTC']
for index,row in ex_info_df.iterrows():
    coin = row.baseAsset
    market = row.symbol
    print('Uploading: {}'.format(coin))
    last_epoch = data_helper.get_last_epoch_binance_raw_data(coin=coin, conn=conn)
    start_epoch = last_epoch + 60000
    klines = api_object.get_historical_klines(market, '1m', start_str=str(start_epoch))
    df = pd.DataFrame(klines, columns=['open_time', 'open', 'high', 'low', 'close', 'volume',
                                       'close_time', 'quote_asset_volume', 'num_trades', 'taker_buy_base_asset_volume',
                                       'taker_buy_quote_asset_volume', 'ignore'])
    df['coin'] = coin
    data_helper.upload_binance_historical_data(df, engine)