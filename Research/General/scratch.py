from Packages.Index.weights import small_cap
from Research.General.helper import key_retriever, get_exchange_df, instantiate_api_object, plan_trades

weights_dict = small_cap()

key_path = '.exchange_keys.json'
key_name = 'Bittrex_Ian'
key_status = 'ro'

exchange, public_key, private_key = key_retriever(key_path,key_name,key_status)

api_object = instantiate_api_object(exchange,public_key, private_key)
exchange_df = get_exchange_df(exchange,api_object)
trade_df = plan_trades(exchange_df,weights_dict)
print(trade_df.head())
