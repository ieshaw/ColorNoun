from Packages.API.General.helper import key_retriever,instantiate_api_object, get_exchange_df
import pandas as pd

# key_path = '.exchange_keys.json'
# key_name = 'Bittrex_Alpha'
# key_status = 'ro'
#
# exchange, public_key, private_key = key_retriever(key_path,key_name,key_status)
# api_object = instantiate_api_object(exchange,public_key,private_key)
# pd.DataFrame(api_object.get_order_history()['result']).to_csv('bit.csv', index=False)

key_path = '.exchange_keys.json'
key_name = 'Binance_Alpha'
key_status = 'ro'

exchange, public_key, private_key = key_retriever(key_path,key_name,key_status)
api_object = instantiate_api_object(exchange,public_key,private_key)
exchange_df = get_exchange_df(exchange, api_object)
out_df = pd.DataFrame()
for index,row in exchange_df.iterrows():
    try:
        market = row.market
        coin_df = pd.DataFrame(api_object.get_my_trades(symbol=market))
        coin_df['market'] = market
        out_df = out_df.append(coin_df, ignore_index=True)
    except Exception as e:
        print(market)
        print(e)
out_df.to_csv('bin.csv', index=False)
