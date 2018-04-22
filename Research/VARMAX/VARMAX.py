__author__ = 'Ian'

import datetime
import pandas as pd
import requests
import os
from statsmodels.tsa.api import VAR
import time
from Execution.Bittrex.bittrex import Bittrex

def get_recent_data(bit2, coins = ['ETH', 'XRP', 'LTC', 'DASH', 'XMR'], freq = 'hour'):
    '''
    :param bit2: bittrex object of v2
    :param coins: list of coin tickers of interest
    :param freq: frequency of ticks, see bittrex.py for details
    :return: pandas dataframe
    '''

    i = 0

    for coin in coins:

        coin_df = pd.DataFrame((bit2.get_candles('BTC-{}'.format(coin), tick_interval= freq)['result']))

        coin_df.index = coin_df['T']

        x_df = pd.DataFrame(index= coin_df['T'])

        x_df['spread_{}'.format(coin)] = coin_df['H'] - coin_df['L']

        x_df[['volumefrom_{}'.format(coin) ,'volumeto_{}'.format(coin)]] = coin_df[['BV' ,'V']]

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

def train_run_VAR(X_df):
    '''
    :param X_df: recent hourly data from
    :return: one line datatframe of predictions for returns of next dataframe
    '''

    VAR_model = VAR(X_df.values)

    results = VAR_model.fit(1)

    prediction = results.forecast(X_df.values[-1,:].reshape(1,20), steps=1)

    pred_df = pd.DataFrame(data=prediction, columns=X_df.columns)

    # Drop columns that are not returns
    for column in pred_df.columns:

        if column.split('_')[0] != 'return':
            pred_df.drop(column, 1, inplace=True)

    return pred_df

def preds_to_weights(pred_df):
    '''
    :param pred_df: one row dictionary of expected returns for next hour
    :return:
    '''

    pred_df = pred_df.where(pred_df > 0, 0)

    sum = float((pred_df.sum(axis = 1)).values)

    out = {}

    for column in pred_df.columns:

        coin = column.split('_')[1]
        out[coin] = float(pred_df[column].values)/ sum

    return out

def trade_on_weights(bit1, bit2, weights):
    '''
    :param bit1: bittrex object of v1.1
    :param bit2: bittrex object of v2
    :param weights: dictionary of desired portfolio allocation, keys are coin tickers, values are floats between 0 and 1
    :return: enacts the trades
    '''

    # Only ever trade with half of available funds

    trade_BTC_bal = 0.5 * (bit1.get_balance('BTC'))['result']['Available']

    # Loop through keys

    for coin in weights:

        #cancel any open orders

        market = 'BTC-{}'.format(coin)

        last_rate = float(bit2.get_latest_candle(market=market, tick_interval='oneMin')['result'][0]['L'])

        trade_BTC = 0.1 * float((bit1.get_balance('BTC'))['result']['Available'])

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

            buy_amount = trade_BTC / last_rate

            if coin_avail < 0.001:

                print('Buying {} of {}'.format(buy_amount, coin))
                print(bit1.buy_limit(market=market, quantity=buy_amount, rate=last_rate))

def run_VARMAX():
    api_key = 'c2402b7f906b4d82b97ca0561d4725ba'
    secret_key = '0bfb77b4b204453eba27c95f2e124e91'

    bit2 = Bittrex(api_key=api_key, api_secret=secret_key, api_version='v2.0')

    bit1 = Bittrex(api_key=api_key, api_secret=secret_key, api_version='v1.1')

    X_df = get_recent_data(bit2, coins = ['ETH', 'XRP', 'LTC', 'DASH', 'XMR'], freq = 'hour')
    pred_df = train_run_VAR(X_df)
    weights = preds_to_weights(pred_df)
    trade_on_weights(bit1, bit2,weights)

while True:
    try:
        # delay until 5 minutes past the hour
        t = datetime.datetime.today()
        future = datetime.datetime(t.year, t.month, t.day, (t.hour + 1) % 24, 5)
        time.sleep((future - t).seconds)
        now = time.ctime(int(time.time()))
        print("________________" + str(now) + "________________")
        run_VARMAX()
        print("________________" + 'End of cycle' + "________________")
    except:
        pass
