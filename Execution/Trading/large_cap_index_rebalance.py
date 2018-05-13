from Packages.Index.weights import large_cap
from Packages.API.General.helper import key_retriever, send_email, trade_on_weights
#load in api keys
key_path = '.exchange_keys.json'
key_name = 'Bittrex_Beta_Large'
key_status = 'ro'
exchange, public_key, private_key = key_retriever(key_path,key_name,key_status)
#find the desired weights by market cap
weights_dict = large_cap()
#make the trades necessary
trade_df = trade_on_weights(exchange, public_key, private_key, weights_dict,
                            min_BTC_prop=0.2)
#send an email notifying
send_email('Rebalancing Large Cap Index Fund. \n\n Trade Plan. \n\n {}'.format(trade_df),
           subj='Large Cap Index Fund Rebalance')