import pandas as pd

def instantiate_api_object(public_key, private_key, api_version='v1.1'):
    '''
    :param public_key:
    :param private_key:
    :param api_version: either 'v1.1' or 'v2.0'
    :return: api object
    '''
    from bittrex.bittrex import Bittrex
    return Bittrex(api_key=public_key, api_secret=private_key, api_version=api_version)

def get_exchange_df(api_object):
    '''
    :param api_object: Bittrex api object
    :return: pandas dataframe with index ticker (string) and
    columns price(float), market(string, market form TICKERBTC), balance(float, amount available)
    '''
    #Get portfolio balance by currency
    balance_df = pd.DataFrame(api_object.get_balances()['result'])
    #Get amount of BTC
    BTC_bal = balance_df.loc[balance_df.Currency == 'BTC','Balance'].values[0]
    #Get the last transacted price by Market
    sum_df = pd.DataFrame(api_object.get_market_summaries()['result'])
    sum_df['BaseCurrency'] = sum_df.MarketName.apply(lambda x: x.split('-')[0])
    #Only transact in BTC base markets
    sum_df = sum_df.loc[(sum_df.BaseCurrency == 'BTC')].copy()
    sum_df['Currency'] = sum_df.MarketName.apply(lambda x: x.split('-')[-1])
    #Merge the two tables
    exchange_df = balance_df.merge(sum_df,on='Currency', how='outer')
    #keep only necessary columns
    exchange_df[['balance','price','ticker','market']] = exchange_df[['Balance','Last','Currency','MarketName']]
    exchange_df = exchange_df[['balance','price','ticker','market']].copy()
    #set the ticker as the index
    exchange_df.set_index('ticker', inplace=True)
    #drop current BTC row
    exchange_df.drop('BTC', axis=0, inplace=True)
    # add BTC Row
    BTC_row = {'price': 1, 'market': 'BTC-BTC', 'balance':BTC_bal}
    exchange_df = exchange_df.append(pd.Series(BTC_row, name='BTC'), ignore_index=False)
    #fill in nans
    exchange_df['balance'].fillna(0,inplace=True)
    return exchange_df

def execute_trades(api_object, trade_df):
    '''
    This functions executes specified trades throught limit orders at most recent price.
    Will change to market orders when Bittrex enables that option.

    param api_object: a bittrex object of version 1.1
    param trade_df: pandas DataFrame with index ticker, columns market (string), price(float, in BTC),
        Curr_Dist(float, [0,1]), Target_Dist(float,[0,1]),Trade_Perc(float,[-1,1]), Trade_Amt (in BTC,float),
        Trade_Amt_Coin (float, in the target currency)
    '''
    for coin,row in trade_df.iterrows():
        #close any open orders
        open_orders = api_object.get_open_orders(market=row.market)['result']
        if open_orders:
            print('Cancelling open orders for {}.'.format(coin))
            for order in open_orders:
                api_object.cancel(uuid=order['OrderUuid'])
        if row.Trade_Amt_Coin > 0:
            print('Buying {} of {}'.format(row.Trade_Amt_Coin, coin))
            print(api_object.buy_limit(market=row.market,
                     quantity=row.Trade_Amt_Coin, rate=row.price))
        elif row.Trade_Amt_Coin < 0:
            print('Selling {} of {}'.format(abs(row.Trade_Amt_Coin), coin))
            print(api_object.sell_limit(market=row.market, quantity=abs(row.Trade_Amt_Coin)
                    , rate=row.price))

def get_recent_data(api_object):
    ''' 
    :param api_object: Bittrex api object
    :param coins: list of coin tickers of interest
    :param freq: frequency of ticks
            can be: oneMin,fiveMin,thirtyMin,hour,day
    :return: pandas dataframe with index datetime and columns Coin_(info) of floats;
    with Price, Volume
    '''
    return 1

