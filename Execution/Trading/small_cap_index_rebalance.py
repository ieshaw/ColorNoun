from Packages.Index.weights import small_cap
from Research.General.helper import key_retriever, trade_on_weights, send_email

weights_dict = small_cap(rank_ceiling=5)

key_path = '.exchange_keys.json'
key_name = 'Bittrex_Beta_Small'
key_status = 'ro'

exchange, public_key, private_key = key_retriever(key_path,key_name,key_status)
trade_df = trade_on_weights(exchange, public_key, private_key, weights_dict, min_BTC_prop=0.2)
send_email('Rebalancing Small Cap Index Fund. \n\n Trade Plan. \n\n {}'.format(trade_df),
           subj='Small Cap Index Fund Rebalance')