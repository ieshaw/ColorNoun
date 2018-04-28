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

def plan_trades(weights,bit1,portfolio_trade_basement=2):
	'''
	This function takes in desired weights for portfolio and plane the trades.
	The trades are filtered to currencies on Bittrex with a BTC pair and
		above a trade basement which is either the Bittrex minumim trade or
		the specified portfolio trade basement.
	The target distribution is chacked and modified if need be to not trade
		beyond portfolio worth.

	param weights: Dictionary of weights with Currency_Ticker:0.XX pairs.
	param portfoli_trade_basement: the minimum trade size in percentage points of 
		portfolio size.
	param bit1: a bittrex object of version 1.1
	return: pandas dateaframe, index is currency tickers, 
		Columns Last (most recent price, float), Curr_Dist(float, [0,1]),
			Target_Dist(float,[0,1]),Trade_Perc(float,[0,1]),
			Trade_Amt (in BTC,float)
	'''
	portfolio_trade_basement /= 100.0
	#Get portfolio balance by currency
	balance_df = pd.DataFrame(bit1.get_balances()['result'])
	#Get amount of BTC
	BTC_bal = balance_df.loc[balance_df.Currency == 'BTC','Balance'].values[0]
	#Get the last transacted price by Market
	sum_df = pd.DataFrame(bit1.get_market_summaries()['result'])
	sum_df['BaseCurrency'] = sum_df.MarketName.apply(lambda x: x.split('-')[0])
	#Only transact in BTC base markets
	sum_df = sum_df.loc[(sum_df.BaseCurrency == 'BTC')].copy()
	sum_df['Currency'] = sum_df.MarketName.apply(lambda x: x.split('-')[-1])
	#Merge the two tables
	comb_df = balance_df.merge(sum_df,on='Currency')
	#keep only necessary columns
	comb_df = comb_df[['Balance','Last','Currency']].copy()
	#Get the amount in BTC by currency
	comb_df.eval('Balance_BTC = Balance * Last', inplace=True)
	#Find total portfolio value in BTC
	BTC_value = BTC_bal + comb_df.Balance_BTC.sum()
	#Set Trade basement as max of desired percentage of portfolio or 
	#the minimum trade on Bittrex
	portfolio_trade_basement = max(portfolio_trade_basement,0.001/BTC_value)
	#Find current distribution of portfolio
	comb_df['Curr_Dist'] = comb_df.Balance_BTC/BTC_value
	#Make the Currencies the index
	comb_df.set_index('Currency', inplace=True)
	#Log Target Distribution
	target_series = pd.Series(weights,name='Target_Dist')
	comb_df = comb_df.join(target_series, how='left')
	#fill in any undescribed coins with 0
	comb_df['Target_Dist'].fillna(0,inplace=True)
	#Check to make sure the target distribution is less than 1.
	#If not, scale appropriately
	dist_sum = (BTC_bal/BTC_value + comb_df.Target_Dist.sum())
	if dist_sum > 1:
		comb_df.Target_Dist /= dist_sum 
	#Find the Trade percentage of portfolio for each currency
	comb_df.eval('Trade_Perc = Target_Dist - Curr_Dist',inplace=True)
	#Drop trade if less than the portfolio basement
	trade_df = comb_df.loc[comb_df.Trade_Perc.abs() > portfolio_trade_basement].copy()
	#Create the Trade Amount
	trade_df['Trade_Amt'] = trade_df.Trade_Perc * BTC_value
	#Trim unecessary columns
	trade_df = trade_df[['Last','Curr_Dist','Target_Dist','Trade_Perc','Trade_Amt']].copy()
	return trade_df

def execute_trades(trade_df,bit1):
	'''
	This functions executes specified trades throught limit orders at most recent price.
	Will change to market orders when Bittrex enables that option.

	param bit1: a bittrex object of version 1.1
	param trade_df: pandas dateaframe, index is currency tickers, 
		Columns Last (most recent price, float), Curr_Dist(float, [0,1]),
			Target_Dist(float,[0,1]),Trade_Perc(float,[0,1]),
			Trade_Amt (in BTC,float)
	'''
	for coin,row in trade_df.iterrows():
		market = 'BTC-{}'.format(coin)
		#close any open orders
		open_orders = bit1.get_open_orders(market=market)['result']
		if open_orders:
			print('Cancelling open orders for {}.'.format(coin))
			for order in open_orders:
				bit1.cancel(uuid=order['OrderUuid'])
		if row.Trade_Amt > 0:
			print('Buying {} of {}'.format(row.Trade_Amt, coin))
			print(bit1.buy_limit(market=market,
					 quantity=row.Trade_Amt, rate=row.Last))
		elif row.Trade_Amt < 0:	
			print('Selling {} of {}'.format(abs(row.Trade_Amt), coin))
			print(bit1.sell_limit(market=market, quantity=abs(row.Trade_Amt)
					, rate=row.Last))

key_json_path = '/Users/ianshaw/.goods/exchange_keys.json'
key_name = 'bittrex_ro'
bit1, bit2 = helper.instantiate_bittrex_objects(key_name,key_json_path)
weights= get_index_weights(bit1)
trade_df = plan_trades(weights,bit1,2)
print(trade_df)
execute_trades(trade_df,bit1)
