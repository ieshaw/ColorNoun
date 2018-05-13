# Color Noun Execution Branch

## EC2 Configuration

### Installing paackages

To install necessary packages run the commands
```angular2html
sudo yum install gcc
pip install urllib3 --upgrade --user
pip install -r requirements.txt --user
```

### Crontab Setup

On the intantiation of EC2 instance execute the command `crontab -e` and provide the following commands.

```angular2html
*/5 * * * * python -m Execution.Trading.arb.py
2 * * * * python -m Execution.Trading.check_portfolio.py
3 8 * * * * python -m Execution.Trading.large_cap_index_rebalace.py
```

### Screen Setting

To ensure that the cron tab operates properly set a screen

```angular2html
screen
```

Then detach 

```angular2html
ctrl+a ctrl+d
```

Before detaching the loacal machine from the instance.

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