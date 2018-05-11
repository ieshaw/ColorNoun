import pandas as pd
from coinmarketcap import Market

def large_cap():
    '''
    return: Dictionary of Coin:market_cap proportion
    '''
    #instantiate coinmarketcap object
    cmc = Market()
    market_df = pd.DataFrame(cmc.ticker())
    #filter out coinse where rank above cieling
    market_df['rank'] = market_df['rank'].astype(int)
    #now weight based on market cap
    market_df['market_cap_usd'] = market_df['market_cap_usd'].astype(float)
    market_df['index_weight'] = market_df['market_cap_usd']/market_df['market_cap_usd'].sum()
    #create dictionary of market and portfolio weights
    weight_dict = dict(zip(market_df.symbol,market_df.index_weight))
    return weight_dict

def small_cap(rank_ceiling = 5):
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