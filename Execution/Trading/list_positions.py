from Packages.API.General.helper import key_retriever, get_exchange_df, instantiate_api_object

key_path = '.exchange_keys.json'
key_name = 'Binance_Alpha'
key_status = 'ro'

exchange, public_key, private_key = key_retriever(key_path,key_name,key_status)
ex_df = get_exchange_df(exchange, instantiate_api_object(exchange,public_key, private_key))
print(ex_df.loc[ex_df.amt_BTC > 0].sort_values('amt_BTC', ascending=False))