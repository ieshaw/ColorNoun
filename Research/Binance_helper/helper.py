import pandas as pd

def instantiate_api_object(public_key, private_key):
    '''
    :param public_key:
    :param private_key:
    :return: api object
    '''
    from binance.client import Client as api_object
    return api_object(public_key, private_key)

def get_exchange_df(api_object):
    '''
    :param api_object: binance api object
    :return: pandas dataframe with index ticker (string) and
    columns price(float), market(string, market form TICKERBTC), balance(float, amount available)
    '''
    exchange_df = pd.DataFrame(api_object.get_account()['balances']).head()
    price_df = pd.DataFrame(api_object.get_all_tickers())
    #create future row for exchange_df
    BTC_row = {'price': 1, 'symbol': 'BTCBTC', 'ticker':'BTC'}
    BTC_row['free'] = exchange_df.loc[exchange_df.asset == 'BTC', 'free'].values[0]
    BTC_row['locked'] = exchange_df.loc[exchange_df.asset == 'BTC', 'locked'].values[0]
    #tease out the ticker from the symbol
    price_df['ticker'] = price_df.symbol.apply(lambda x: x.split('BTC')[0])
    # drop non BTC Markets
    price_df = price_df.loc[price_df.ticker != price_df.symbol].copy()
    #merge the two dataframes
    exchange_df = price_df.merge(exchange_df, how='left', left_on='ticker', right_on='asset')
    #append the BTC Row
    exchange_df = exchange_df.append(BTC_row, ignore_index=True)
    #rename columns
    exchange_df[['market', 'balance']] = exchange_df[['symbol', 'free']]
    #drop the unecessary asset column
    exchange_df = exchange_df[['price', 'market','ticker', 'balance']].copy()
    # exchange_df.drop(['asset', 'locked','symbol', 'free'], axis=1, inplace=True)
    #any missing balance, make 0
    exchange_df.fillna(0, inplace=True)
    #fix the types
    exchange_df.balance = exchange_df.balance.astype(float)
    exchange_df.price = exchange_df.price.astype(float)
    #set the ticker as the index
    exchange_df.set_index('ticker', inplace=True)
    return exchange_df

def execute_trades(api_object,trade_df):
    '''
    :param api_object: binance api object
    :param trade_df:
    :return: pandas dataframe of trade request json responses from exchange API
    '''
    return 1

def get_recent_data(api_object):
    '''
    :param api_object: binance api object
    :return: pandas dataframe with index datetime and columns Coin_(info) of floats;
    with Price, Volume
    '''
    return 1
