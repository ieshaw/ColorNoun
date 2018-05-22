from Packages.API.General.helper import key_retriever,instantiate_api_object
import pandas as pd

key_path = '.exchange_keys.json'
key_name = 'Binance_Alpha'
key_status = 'ro'

exchange, public_key, private_key = key_retriever(key_path,key_name,key_status)
api_object = instantiate_api_object(exchange, public_key, private_key)
ex_info_df = pd.DataFrame(api_object.get_exchange_info()['symbols'])
ex_info_df = ex_info_df.loc[ex_info_df.quoteAsset == 'BTC']
market_cap_dict = {}
for index,row in ex_info_df.iterrows():
    coin = row.baseAsset
    market = row.symbol
    print(coin, market)