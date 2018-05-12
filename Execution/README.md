# Color Noun Execution Branch

## Website

This houses any python code necessary for rendering the website.

## Exchange Keys

The exchange keys json has the following information as a dictionary:
* Key: `name`
* Value: a dictionary
    * Key: status `live` (trading privileges) or `ro` (read only)
    * Value: a dictionary
        * Key:`exchange`, the exchange name name
        * Key: `public`, the public key
        * Key: `private`, the private key 
        
## Trading

This houses all our code for execution of algorithms. The current this is a summary of our 
current strategies.

### Strategy Overviews

This section is meant to convey a high level understanding of each strategy.

#### Large Cap Index

This is a index with daily rebalancing weighting exposure to coins 
proportional to market capitalization.

#### Small Cap Index

Similar to the Large Cap Index, this is a index with daily rebalancing weighting exposure to coins 
proportional to market capitalization. The difference is that it only weighs in on coins outside the 
top teir. As of now, this means that the weighting starts with the 8th ranked coin by market cap. 
The hope is to extend exposure deeper into the cryptocurrency market.

#### Alpha VARX

This is a alpha strategy meant to capture regressive dependencies between coins and their technical aspect 
(spread, volume, returns). 

#### Alpha Exchange Arbitrage

This is an alpha strategy in development, with intent to capitalize upon pricing differences between exchanges. 