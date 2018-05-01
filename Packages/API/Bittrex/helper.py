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
    comb_df = balance_df.merge(sum_df,on='Currency', how='outer')
    #keep only necessary columns
    comb_df = comb_df[['Balance','Last','Currency']].copy()
    #fill in nans
    comb_df['Balance'].fillna(0,inplace=True)
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
    trade_df['Trade_Amt_BTC'] = trade_df.Trade_Perc * BTC_value
    #The Trade amount in the Coin
    trade_df.eval('Trade_Amt_Coin = Trade_Amt_BTC/Last',inplace=True)
    #Rename column
    trade_df['Last_Price_BTC'] = trade_df['Last']
    #Trim unecessary columns
    trade_df = trade_df[['Last_Price_BTC','Curr_Dist','Target_Dist','Trade_Perc',
                 'Trade_Amt_BTC', 'Trade_Amt_Coin']].copy()
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
        if row.Trade_Amt_Coin > 0:
            print('Buying {} of {}'.format(row.Trade_Amt_Coin, coin))
            print(bit1.buy_limit(market=market,
                     quantity=row.Trade_Amt_Coin, rate=row.Last_Price_BTC))
        elif row.Trade_Amt_Coin < 0:
            print('Selling {} of {}'.format(abs(row.Trade_Amt_Coin), coin))
            print(bit1.sell_limit(market=market, quantity=abs(row.Trade_Amt_Coin)
                    , rate=row.Last_Price_BTC))

def trade_on_weights(weights,bit1,portfolio_trade_basement=1):
    '''
    This function executes trades for a portfolio toward target weights.

    param weights: Dictionary of weights with Currency_Ticker:0.XX pairs.
    param portfoli_trade_basement: the minimum trade size in percentage points of
        portfolio size.
    param bit1: a bittrex object of version 1.1
    '''
    trade_df = plan_trades(weights,bit1,2)
    print('--------------------Trade Plan-----------------')
    print(trade_df)
    print('----------------------------------------------')
    execute_trades(trade_df,bit1)
