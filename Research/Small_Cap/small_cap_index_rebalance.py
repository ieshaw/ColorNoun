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

def get_portfolio_value_BTC(balance_df):
    '''
    :param balance_df: pandas datafram with columns asset (ticker), free (float), last(float)
    :return: float, value of portfolio in BTC
    '''

key_json_path = '.binance_exchange_keys.json'
key_name = 'beta_ro'

client = Client(*key_retriever(key_json_path,key_name))
# index_weights = get_small_cap_index_weights(rank_ceiling=8)
# index_weights = redistribute_weights_for_binance(client, index_weights, portfolio_worth_BTC=0.1)
balance_df = pd.DataFrame(client.get_account()['balances']).head()
price_df = pd.DataFrame(client.get_all_tickers())
price_df['ticker'] = price_df.symbol.apply(lambda x: x.split('BTC')[0])
#drop non BTC Markets
price_df = price_df.loc[price_df.ticker != price_df.symbol].copy()
print(price_df.head())