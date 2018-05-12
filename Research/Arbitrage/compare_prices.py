from Packages.API.General.helper import key_retriever, instantiate_api_object, get_exchange_df

key_path = '.exchange_keys.json'
key_name = 'Bittrex_Beta_Large'
key_status = 'ro'

exchange, public_key, private_key = key_retriever(key_path,key_name,key_status)
api_object = instantiate_api_object(exchange,public_key, private_key)
bittrex_df = get_exchange_df(exchange, api_object)[['price']]

key_path = '.exchange_keys.json'
key_name = 'Binance_Alpha'
key_status = 'ro'

exchange, public_key, private_key = key_retriever(key_path,key_name,key_status)
api_object = instantiate_api_object(exchange,public_key, private_key)
binance_df = get_exchange_df(exchange, api_object)[['price']]

comb_df = bittrex_df.join(binance_df, how='inner', lsuffix='_bittrex', rsuffix='_binance')
comb_df.eval('space = 1 - price_bittrex/price_binance', inplace=True)
comb_df = comb_df.loc[comb_df.space.abs() > 0.005].copy()

binance_weights_df = comb_df.loc[comb_df.space > 0].copy()
binance_weights_dict = (binance_weights_df.space.abs()/(binance_weights_df.space.abs().sum())).to_dict()
print(binance_weights_dict)

bittrex_weights_df = comb_df.loc[comb_df.space < 0].copy()
bittrex_weights_dict = (bittrex_weights_df.space.abs()/(bittrex_weights_df.space.abs().sum())).to_dict()
print(bittrex_weights_dict)