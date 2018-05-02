import pandas as pd
from Packages.API.Bittrex import helper

key_json_path = '.exchange_keys.json'
key_name = 'bittrex_alpha_ro'
bit1, bit2 = helper.instantiate_bittrex_objects(key_name, key_json_path)

# Get portfolio balance by currency
balance_df = pd.DataFrame(bit1.get_balances()['result'])
balance_df = balance_df.query('Balance > 0').copy()
current_coins = balance_df.loc[balance_df['Currency'] != 'BTC', 'Currency'].unique()
all_sell_dict = {coin:0 for coin in current_coins}
helper.trade_on_weights(weights=all_sell_dict, bit1=bit1, portfolio_trade_basement=0.0)