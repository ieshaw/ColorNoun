from Packages.API.General.helper import key_retriever, all_to_BTC

key_path = '.exchange_keys.json'
key_name = 'Binance_Alpha'
key_status = 'ro'

exchange, public_key, private_key = key_retriever(key_path,key_name,key_status)
trade_df = all_to_BTC(exchange,public_key, private_key)