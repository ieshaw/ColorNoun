__author__ = 'Ian'

#general python packages
import pandas as pd

#Tridens Packages
from Packages.API.Bittrex.bittrex import Bittrex
from Packages.API.Helper.helper import key_retriever

def instantiate_bittrex_objects(key_name,key_json_path):
	'''
	This function is meant to simplify the process of instantiating bittrex objects.

	param key_name: the key in the json dictionary whose value is the api keys
	param key_json_path: the path to the json file holding the dictionary of dictionaries
				of api keys
	'''
	api_key,secret_key = key_retriever(key_json_path,key_name)
	bit2 = Bittrex(api_key=api_key, api_secret=secret_key, api_version='v2.0')
	bit1 = Bittrex(api_key=api_key, api_secret=secret_key, api_version='v1.1')
	return bit1,bit2        

def get_recent_data(bit2, coins = ['ETH', 'XRP', 'LTC', 'DASH', 'XMR'], freq = 'hour'):
	'''
	A function to pull in available recent data from the Bittrex API.
	Normalizes the volume and spred

	:param bit2: bittrex object of v2
	:param coins: list of coin tickers of interest
	:param freq: frequency of ticks
			can be: oneMin,fiveMin,thirtyMin,hour,day
	:return: pandas dataframe with columns TICKER_volume,TICKER_spread,TICKER_return
		by the frequency
	'''
	i = 0
	for coin in coins:
		coin_df = pd.DataFrame((bit2.get_candles('BTC-{}'.format(coin),
					 tick_interval= freq)['result']))
		coin_df.index = coin_df['T']
		x_df = pd.DataFrame(index= coin_df['T'])
		x_df['spread_{}'.format(coin)] = coin_df['H'] - coin_df['L']
		x_df[['volumefrom_{}'.format(coin) ,
			'volumeto_{}'.format(coin)]] = coin_df[['BV' ,'V']]
		normal_len = 5
		x_df = (x_df - x_df.rolling(window= normal_len, min_periods= normal_len).mean())\
		       /x_df.rolling(window=normal_len, min_periods=normal_len).std()
		ret_df = coin_df['C'].pct_change()
		x_df['return_{}'.format(coin)] = ret_df
		x_df = x_df.dropna()
		if i == 0:
		    X_df = x_df
		    i = 1
		else:
		    X_df = X_df.join(x_df, how = 'inner')
	return X_df

def get_portfolio_worth_in_BTC(bit1):
	'''
	Function to calculate the BTC worth of the current portfolio on Bittrex.
	:param bit1: Bittrex object v1
	return: the portfolio worth in BTC	
	'''
	#Get portfolio balance by currency
	balance_df = pd.DataFrame(bit1.get_balances()['result'])
	#Get the last transacted price by Market
	sum_df = pd.DataFrame(bit1.get_market_summaries()['result'])
	sum_df['BaseCurrency'] = sum_df.MarketName.apply(lambda x: x.split('-')[0])
	#Only transact in BTC base markets
	sum_df = sum_df.loc[(sum_df.BaseCurrency == 'BTC')].copy()
	sum_df['Currency'] = sum_df.MarketName.apply(lambda x: x.split('-')[-1])
	#Merge the two tables
	comb_df = balance_df.merge(sum_df,on='Currency')
	#Get the Current BTC balance
	BTC_val = balance_df.loc[balance_df.Currency == 'BTC','Balance'].values[0]
	#Add the converted value of all other coins
	BTC_val += comb_df.eval('Balance*Last').sum()
	return BTC_val

def trade_on_weights(bit1, bit2, weights,trade_basement_perc=1):
	'''
	This function changes the portfolio allocation to the specified proportional weights.
	This uses limit orders at the most recent recorded transaction price.
	Bittrex	does not support market orders.

	:param bit1: bittrex object of v1.1
	:param bit2: bittrex object of v2
	:param weights: dictionary of desired portfolio allocation, keys are coin tickers, values are floats between 0 and 1
	'''
	trade_BTC_bal = get_portfolio_worth_in_BTC(bit1) 
	#only trade if trade casues trade_basement_perc% difference in holdings
	#this is to avoind paying transaction fees on small changes
	min_trade = 0.01*trade_basement_perc*trade_BTC_bal
	# Loop through keys
	for coin in weights:
		market = 'BTC-{}'.format(coin)
		#check if currency is traded in bittrex
		if market not in bit1.list_markets_by_currency(coin):
			print('{} is not traded on Bittrex.'.format(market))
			#If not traded on bittrex, forget about it
			continue
		#Find then current going rate of the coin
		last_rate = float(bit2.get_latest_candle(market=market, tick_interval='oneMin')['result'][0]['L'])
		#cancel any open orders
#		open_orders = bit1.get_open_orders(market='BTC-{}'.format(coin))['result']
#		if open_orders:
#			for order in open_orders:
#				bit1.cancel(uuid=order['OrderUuid'])
		#find balance of the currency in question
		coin_avail = (bit1.get_balance(coin))['result']['Available']
		if coin_avail is None:
			coin_avail = 0
		#find the difference between our amount and the desried amount
		desired_amount = weights[coin] * trade_BTC_bal / last_rate
		trade_amount = desired_amount - coin_avail
		print('{}.Current Position: {:.2E}. Desired Position: {:.2E}.'.format(
			coin,coin_avail,desired_amount))
		trade_size_BTC = abs(trade_amount*last_rate)
		if trade_size_BTC > min_trade: 
			# if Sell
			if trade_amount < -0.0001:
				print('Selling {} of {}'.format(abs(trade_amount), coin))
#				print(bit1.sell_limit(market=market, quantity=abs(trade_amount)
#					, rate=last_rate))
			#if Buy
			elif trade_amount > 0.001: 
				print('Buying {} of {}'.format(trade_amount, coin))
#				print(bit1.buy_limit(market=market,
#					 quantity=trade_amount, rate=last_rate))
		elif abs(trade_amount) > 0:
			print('Not trading. {:2E} BTC worth of {} is below {}% of portfolio[{:2E} BTC].'.format(
		trade_size_BTC,coin,trade_basement_perc,min_trade))
