__author__ = 'Ian'

import pandas as pd
import requests
import os
from statsmodels.tsa.api import VAR
import time
from Execution.Bittrex.bittrex import Bittrex


bit1 = Bittrex(api_key=api_key, api_secret=secret_key, api_version='v1.1')
bit2 = Bittrex(api_key=api_key, api_secret=secret_key, api_version='v2.0')


for coin in bit1.get_currencies()['result']:

    ticker = coin['Currency']

    print(ticker)

    if ticker == 'BTC':
        continue

    try:

        market = 'BTC-{}'.format(ticker)
        last_rate = float(bit2.get_latest_candle(market=market, tick_interval='oneMin')['result'][0]['L'])
        
        open_orders = bit1.get_open_orders(market=market)['result']

        if open_orders:

            for order in open_orders:
                bit1.cancel(uuid=order['OrderUuid'])

        coin_avail = (bit1.get_balance(ticker))['result']['Available']

        if coin_avail is None:
            coin_avail = 0

        # if weight is 0 and we have some

        if coin_avail > 0:
            # sell it all

            print('Selling {} of {}'.format(coin_avail, ticker))

            print(bit1.sell_limit(market=market, quantity=coin_avail, rate=last_rate))

    except:
        continue
