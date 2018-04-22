
__author__ = 'Ian'

from Packages.API.Bittrex.bittrex import Bittrex
import pandas as pd
from coinmarketcap import Market

def trade_on_weights(bit1, bit2, weights):

    '''
    :param bit1: bittrex object of v1.1
    :param bit2: bittrex object of v2
    :param weights: dictionary of desired portfolio allocation, keys are coin tickers, values are floats between 0 and 1
    :return: enacts the trades
    '''

    # Only ever trade with half of available funds

    trade_BTC_bal = (bit1.get_balance('BTC'))['result']['Available']

    # Loop through keys

    for coin in weights:

        #cancel any open orders

        market = 'BTC-{}'.format(coin)

	#check if currency is traded in bittrex
	if market not in bit1.list_markets_by_currency(coin):
		print('{} is not traded on Bittrex.'.format(market))
		continue

        last_rate = float(bit2.get_latest_candle(market=market, tick_interval='oneMin')['result'][0]['L'])

        open_orders = bit1.get_open_orders(market='BTC-{}'.format(coin))['result']

        if open_orders:

            for order in open_orders:

                bit1.cancel(uuid=order['OrderUuid'])

        coin_avail = (bit1.get_balance(coin))['result']['Available']

        if coin_avail is None:
            coin_avail = 0

        # if weight is 0 and we have some

        if weights[coin] < 0.0025 and coin_avail > 0:

            # sell it all

            print('Selling {} of {}'.format(coin_avail, coin))

            print(bit1.sell_limit(market=market, quantity=coin_avail, rate=last_rate))

        # if weight is > 0

        else:

            # if already invested in the coin, leave it, no need to call on extra transaction costs

            # if we do not have any

            buy_amount = weights[coin] * trade_BTC_bal / last_rate

            if coin_avail < 0.001:

                print('Buying {} of {}'.format(buy_amount, coin))
                print(bit1.buy_limit(market=market, quantity=buy_amount, rate=last_rate))

def get_index_weights():
	#instantiate coinmarketcap object
	cmc = Market()
	market_df = pd.DataFrame(cmc.ticker())

	#only concerned with the top 10 coins for now
	market_df = market_df.loc[market_df['rank'].astype(int) < 11].copy()

	#now weight based on market cap
	market_df['market_cap_usd'] = market_df['market_cap_usd'].astype(float)
	market_df['index_weight'] = market_df['market_cap_usd']/market_df['market_cap_usd'].sum()

	#for now, just drop the BTC enty
	market_df = market_df.loc[market_df['symbol'] != 'BTC'].copy()

	#create dictionary of market and portfolio weights
	weight_dict = dict(zip(market_df.symbol,market_df.index_weight))

	return weight_dict

def run_index():

    api_key = 'c2402b7f906b4d82b97ca0561d4725ba'
    secret_key = '0bfb77b4b204453eba27c95f2e124e91'

    bit2 = Bittrex(api_key=api_key, api_secret=secret_key, api_version='v2.0')

    bit1 = Bittrex(api_key=api_key, api_secret=secret_key, api_version='v1.1')

    weights = get_index_weights()
    trade_on_weights(bit1, bit2,weights)

print('Rebalancing Index Fund')
run_index()
