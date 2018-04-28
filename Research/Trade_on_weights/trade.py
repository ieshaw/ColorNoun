__author__ = 'Ian'

from Packages.API.Bittrex import helper
from Packages.API.Bittrex.bittrex import Bittrex
import pandas as pd
from coinmarketcap import Market

def get_index_weights(bit1):
	'''
	param bit1: bittrex object of v1.1
	return: Dictionary of Coin:market_cap proportion
	'''
	#instantiate coinmarketcap object
	cmc = Market()
	market_df = pd.DataFrame(cmc.ticker())
	#Keep only coins traded on bittrex
	market_df = market_df.loc[market_df['symbol'].isin(
		pd.DataFrame(bit1.get_currencies()['result']).Currency.unique())].copy()
	#now weight based on market cap
	market_df['market_cap_usd'] = market_df['market_cap_usd'].astype(float)
	market_df['index_weight'] = market_df['market_cap_usd']/market_df['market_cap_usd'].sum()
	#find minimum Bittrex trade size, as function of
	#portfolio value. Currently 0.001 BTC.
	#Only trade 2x the minimum
	#That way we can get out if moves against us
	min_perc = 2 * 0.001/(helper.get_portfolio_worth_in_BTC(bit1))
	#filter to only trade if above percentage threshold
	market_df['index_weight'] = market_df['index_weight'].where(
		market_df['index_weight'] >min_perc,0)
	#rebalance to reflect current weight distribution
	market_df['index_weight'] = market_df['index_weight']/market_df['index_weight'].sum()
	market_df['index_weight'].fillna(0,inplace=True)
	#Since Base currency is BTC, do not trade 
	market_df = market_df.loc[market_df['symbol'] != 'BTC'].copy()
	#create dictionary of market and portfolio weights
	weight_dict = dict(zip(market_df.symbol,market_df.index_weight))
	return weight_dict

key_json_path = '/Users/ianshaw/.goods/exchange_keys.json'
key_name = 'bittrex_ro'
bit1, bit2 = helper.instantiate_bittrex_objects(key_name,key_json_path)
weights= get_index_weights(bit1)
helper.trade_on_weights(weights,bit1)
