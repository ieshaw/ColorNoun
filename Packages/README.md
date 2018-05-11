# Packages

This is the directory of the Tridens Capital repository where all software packages will be housed and available for import by team members. 

## Package Use

Since all scripts are designed to be run from the Tridens home directory, at the top of any script simply import directly from the file in the Packages directory.

```
from Packages.subdir.file import module
```

## Available Packages

 - API
    * Bittrex
        + `helper`: functions specific to executing on the Bittrex exchange
    * Binance
        + `helper`: functions specific to executing on the Binance exchange
  * Helper
    + `helper`: functions to support api interface (ex: retrieve_key)
  * Trade
    + `trade`: This is meant to abstract away exchange specific dynamics. 
        Taking in the intended portfolio weights and a key dictionary as arguments. 
- Index
    * `weights`: holds functions for index weights.        


### Note on Exchange API helpers

These helpers are meant to abstract away from the API interface. 
The centerpiece of the `Helper.helper` is a `trade_on_weights` function. This funciton
allows for intended weightings to be passed in and eventually excuted as trades. 
This function calls upon the following functions from each exchange-specific helper.
1. `intantiate_exchange_object`: Create the object necessary for interacting with exchange api.
2. `generate_exchange_df`: Creates a dataframe of with 
the price, portfolio propotional holdings on that specific exchange account.
3. `execute_trades`: Excutes Trades on Exchange.

These functions run the weighting through the following filters:
1. Above minimum trade size for exchange
2. Above a trade basement, currently 1%. 
This means no trade is executed unless it changes the portfolio value more than 1%, 
meant to minimize small trades that cause high transaction costs, only taking significant positions.

3. Maintain a certain BTC level in each wallet. 
This sure at least XX% of any portfolio is in BTC. 
This allows for BTC to be available for rebalance buys at each transaction period.
 For index funds this is 20%, and 50% for alpha funds.

4. Makes sure there are enough BTC available for each trade. 

The Generic helper uses the `exchange_df` and an input `weights_dict` to create a `trade_df` 
which is used to execute trades. All trading scripts should only import the general helper functions, 
not the exchange specific API helpers.