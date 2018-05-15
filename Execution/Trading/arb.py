from Packages.API.General.helper import key_retriever, instantiate_api_object, get_exchange_df, \
    trade_on_weights, send_email

# Load in API Keys
key_dict = {}
#Bittrex
key_path = '.exchange_keys.json'
key_name = 'Bittrex_Alpha'
key_status = 'live'
exchange, public_key, private_key = key_retriever(key_path,key_name,key_status)
key_dict['Bittrex'] = [exchange, public_key, private_key]
api_object = instantiate_api_object(exchange, public_key, private_key)
bittrex_df = get_exchange_df(exchange, api_object)[['price']]
#Binance
key_path = '.exchange_keys.json'
key_name = 'Binance_Alpha'
key_status = 'live'
exchange, public_key, private_key = key_retriever(key_path,key_name,key_status)
key_dict['Binance'] = [exchange, public_key, private_key]
api_object = instantiate_api_object(exchange,public_key, private_key)
binance_df = get_exchange_df(exchange, api_object)[['price']]
#Compare the prices
comb_df = bittrex_df.join(binance_df, how='inner', lsuffix='_bittrex', rsuffix='_binance')
comb_df.eval('space = 1 - price_binance/price_bittrex', inplace=True)
comb_df = comb_df.loc[comb_df.space.abs() > 0.007].copy()
#Buy Binance if lower
binance_weights_df = comb_df.loc[comb_df.space > 0].copy()
binance_weights_dict = (binance_weights_df.space.abs()/(binance_weights_df.space.abs().sum())).to_dict()
#Buy Bittrex if lower
bittrex_weights_df = comb_df.loc[comb_df.space < 0].copy()
bittrex_weights_dict = (bittrex_weights_df.space.abs()/(bittrex_weights_df.space.abs().sum())).to_dict()
#Trade Binance
exchange, public_key, private_key = key_dict['Binance']
bin_trade_df = trade_on_weights(exchange, public_key, private_key, binance_weights_dict,
                            min_BTC_prop=0.5)
#Trade Bittrex
exchange, public_key, private_key = key_dict['Bittrex']
bit_trade_df = trade_on_weights(exchange, public_key, private_key, bittrex_weights_dict,
                            min_BTC_prop=0.5)
#send an email notifying
send_email('Executing Arbitrage Play. \n\n Binance Trade Plan. \n\n {}\n\nBinance Trade Plan. \n\n {}'.format(
    bin_trade_df, bit_trade_df),subj='Arbitrage Trade Update')
# print('Executing Arbitrage Play. \n\n Binance Trade Plan. \n\n {}\n\n Bittrex Trade Plan. \n\n {}'.format(
#     bin_trade_df, bit_trade_df))