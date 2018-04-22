__author__ = 'Ian'

#general python packages
import pandas as pd

#Tridens Packages
from Packages.API.Bittrex.bittrex import bittrex

def get_recent_data(bit2, coins = ['ETH', 'XRP', 'LTC', 'DASH', 'XMR'], freq = 'hour'):

	'''
	A function to pull in available recent data from the Bittrex API.
	Normalizes the volume and spred

	:param bit2: bittrex object of v2
	:param coins: list of coin tickers of interest
	:param freq: frequency of ticks
			can be: oneMin,fiveMin,thirtyMin,hour,day
	:return: pandas dataframe with columns volume,spread,return
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
