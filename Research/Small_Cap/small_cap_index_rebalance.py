__author__ = 'Ian'

from Packages.API.Helper.helper import key_retriever
from binance.client import Client
from coinmarketcap import Market
import pandas as pd

def get_small_cap_index_weights(rank_ceiling = 5):
    '''
    param rank_ceiling: integer, the highest rank by market cap that
        can be in the index. For example, if 5, the heaviest weighted coin
        will be the coin with the fifth larget market cap
    return: Dictionary of Coin:market_cap proportion
    '''
    #instantiate coinmarketcap object
    cmc = Market()
    market_df = pd.DataFrame(cmc.ticker())
    #filter out coinse where rank above cieling
    market_df['rank'] = market_df['rank'].astype(int)
    market_df = market_df.loc[market_df['rank'] >= rank_ceiling].copy()
    #now weight based on market cap
    market_df['market_cap_usd'] = market_df['market_cap_usd'].astype(float)
    market_df['index_weight'] = market_df['market_cap_usd']/market_df['market_cap_usd'].sum()
    #create dictionary of market and portfolio weights
    weight_dict = dict(zip(market_df.symbol,market_df.index_weight))
    return weight_dict

def redistribute_weights_for_binance(client, weights_dict, portfolio_worth_BTC):
    '''
    This function works to redistribute the weights so that they are above the Binance trade threshold
        (actually twice the threshold to be safe), and makes sure they are listed on binance.
    param client: a binance client object
    :param weights_dict: a dictionary of Ticker(string):weights(float)
    :param portfolio_worth_BTC: float, worth of current portfolio in BTC
    :return: dictionary of weights to trade.
    '''
    #Turn the dictionary into a pandas series
    weights_series = pd.Series(weights_dict)
    #join on coins offered as BTC pairs on Binance
    info_df = pd.DataFrame(client.get_exchange_info()['symbols'])
    binance_tickers = info_df.loc[info_df.quoteAsset == 'BTC'].baseAsset.unique()
    weights_series = weights_series.loc[weights_series.index.isin(binance_tickers)].copy()
    #Drop any below the Binance trade threshold
    binance_min_BTC = 0.001
    min_perc = 2 * binance_min_BTC/portfolio_worth_BTC
    #Find the trade threshold as a function of our current portfolio
    weights_series = weights_series.loc[weights_series.values > min_perc].copy()
    #Redistribute the weights
    weights_series = weights_series/(weights_series.sum())
    return weights_series.to_dict()

def get_balance_df(client):
    '''
    :param client: binance client object
    :return: pandas dataframe with columns price(float), symbol(string, market form TICKERBTC),
        ticker(string), free (float, amount available), locked(float, amount unavailable),
        amt_BTC(float, amount of each coin in BTC)
    '''
    balance_df = pd.DataFrame(client.get_account()['balances']).head()
    price_df = pd.DataFrame(client.get_all_tickers())
    #create future row for balance_df
    BTC_row = {'price': 1, 'symbol': 'BTCBTC', 'ticker':'BTC'}
    BTC_row['free'] = balance_df.loc[balance_df.asset == 'BTC', 'free'].values[0]
    BTC_row['locked'] = balance_df.loc[balance_df.asset == 'BTC', 'locked'].values[0]
    #tease out the ticker from the symbol
    price_df['ticker'] = price_df.symbol.apply(lambda x: x.split('BTC')[0])
    # drop non BTC Markets
    price_df = price_df.loc[price_df.ticker != price_df.symbol].copy()
    #merge the two dataframes
    balance_df = price_df.merge(balance_df, how='left', left_on='ticker', right_on='asset')
    #drop the unecessary asset column
    balance_df.drop('asset', axis=1, inplace=True)
    #append the BTC Row
    balance_df = balance_df.append(BTC_row, ignore_index=True)
    #any missing free or locked, make 0
    balance_df.fillna(0, inplace=True)
    #fix the types
    balance_df.free = balance_df.free.astype(float)
    balance_df.locked = balance_df.locked.astype(float)
    balance_df.price = balance_df.price.astype(float)
    #make amt BTC column
    balance_df.eval('amt_BTC = free * price', inplace=True)
    return balance_df

def plan_trades(balance_df, weights_dict, BTC_prop= 0.2, min_trade_prop=0.005):
    '''
    :param balance_df: pandas dataframe with columns price(float), symbol(string, market form TICKERBTC),
        ticker(string), free (float, amount available), locked(float, amount unavailable),
        amt_BTC(float, amount of each coin in BTC)
    :param weights_dict: dictionary,
        key:value Ticker(string):weight(float). weights must sum to one
    :param BTC_prop: float, proportion of portfolio that must stay BTC,
        This allows for reserves to buy and sell with. Default 0.2 (20%)
    :param min_trade_prop: float, minimum trade as proportion of portfolio. Default is 0.005,
            indicating that will not trade unless trade size is greater than 0.5% of portfolio.
            Designed to minumize portfolio loss due to transaction costs on small trades.
    :return: pandas dataframe with index Currency (string) with float entries in columns
        Curr_Dist, Target_Dist, Trade_Amt_Coin
    '''
    #create pandas series of weights dict
    weights_series = pd.Series(weights_dict, name='Target_Dist')
    #make sure weights sum to 1
    weights_series = weights_series/(weights_series.sum())
    #turn the ticker into the index
    balance_df['Currency'] = balance_df['ticker']
    balance_df.set_index('Currency', inplace=True)
    balance_df.drop('ticker', axis=1, inplace=True)
    #merge the weights onto current balances
    trade_df = balance_df.join(weights_series)
    trade_df.Target_Dist.fillna(0, inplace=True)
    #get current distribution
    trade_df['Curr_Dist'] = trade_df.amt_BTC/(trade_df.amt_BTC.sum())
    #get our current available BTC
    avail_BTC = trade_df.loc[trade_df.index == 'BTC', 'amt_BTC']
    #reset the target distributions to compensate for BTC liquidity requirements
    trade_df.drop('BTC', axis=0, inplace=True)
    trade_df.Target_Dist = (1 - BTC_prop)* trade_df.Target_Dist/(trade_df.Target_Dist.sum())
    #Find the trade size in terms of percentage for portfolio

    print(trade_df)






'''

def trade_on_weights(client, weights_dict, return_df=True):

    balance_df = get_balance_df(client)
    redistributed_weights_dict = redistribute_weights_for_binance(client, weights_dict,
                                                    portfolio_worth_BTC= balance_df.amt_BTC.sum())
    trade_df = plan_trades(balance_df, redistributed_weights_dict)
    execute_trades(trade_df)

    if return_df:
        return trade_df

def instantiate_and_trade_on_weights(key_json_path, key_name, weights_dict, return_df=True):

    client = Client(*key_retriever(key_json_path, key_name))
    trade_df= trade_on_weights(client, weights_dict, return_df=True)
    if return_df:
        return trade_df

 '''



key_json_path = '.binance_exchange_keys.json'
key_name = 'beta_ro'

client = Client(*key_retriever(key_json_path,key_name))
# index_weights = get_small_cap_index_weights(rank_ceiling=8)
balance_df = get_balance_df(client)
#at like we have 1 BTC
balance_df.loc[balance_df.ticker == 'BTC', 'amt_BTC'] = 1
balance_df.loc[balance_df.ticker == 'BTC', 'free'] = 1
weights_dict = get_small_cap_index_weights()
redistributed_weights_dict = redistribute_weights_for_binance(client, weights_dict,
                                                    portfolio_worth_BTC= balance_df.amt_BTC.sum())
plan_trades(balance_df,weights_dict)