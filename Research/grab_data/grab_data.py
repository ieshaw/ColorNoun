from Packages.API.General.helper import key_retriever, instantiate_api_object
import pandas as pd

key_path = '.exchange_keys.json'
key_name = 'Binance_Alpha'
key_status = 'ro'

exchange, public, private = key_retriever(key_path, key_name)
api_object = instantiate_api_object(exchange, public, private)
coin = 'ETH'
market = 'ETHBTC'
#furthest I could go back
start_epoch = 1500004800000
klines = api_object.get_historical_klines(market, '1m', start_str=str(start_epoch))
df = pd.DataFrame(klines, columns=['open_time', 'open', 'high', 'low', 'close', 'volume',
                                   'close_time', 'quote_asset_volume', 'num_trades', 'taker_buy_base_asset_volume',
                                   'taker_buy_quote_asset_volume', 'ignore'])
df['coin'] = coin
df.to_csv('{}.csv'.format(coin), index=False)
