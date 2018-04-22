
__author__ = 'Ian'

from Packages.API.Bittrex import helper
import pandas as pd
from coinmarketcap import Market

def get_index_weights():
	'''
	return: Dictionary of Coin:market_cap proportion
	'''

	#instantiate coinmarketcap object
	cmc = Market()
	market_df = pd.DataFrame(cmc.ticker())

	#now weight based on market cap
	market_df['market_cap_usd'] = market_df['market_cap_usd'].astype(float)
	market_df['index_weight'] = market_df['market_cap_usd']/market_df['market_cap_usd'].sum()

	#for now, just drop the BTC enty
	market_df = market_df.loc[market_df['symbol'] != 'BTC'].copy()

	#create dictionary of market and portfolio weights
	weight_dict = dict(zip(market_df.symbol,market_df.index_weight))

	return weight_dict

def run_index():
	'''
	This function gathers the index weights and instructs bittrex to move our portfolio
	to those weights.
	'''
	key_json_path = '/Users/ianshaw/.goods/exchange_keys.json'
	key_name = 'bittrex'
	bit1, bit2 = helper.instantiate_bittrex_objects(key_name,key_json_path)
	weights = get_index_weights()
	trade_on_weights(bit1, bit2,weights)

print('Rebalancing Index Fund')
run_index()
