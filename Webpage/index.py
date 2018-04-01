#!/home/tridxmod/mypython/bin/python

from bittrex import Bittrex
#Load API
api_key = 'c2402b7f906b4d82b97ca0561d4725ba'
secret_key = '0bfb77b4b204453eba27c95f2e124e91'
bit = Bittrex(api_key=api_key, api_secret=secret_key, api_version='v2.0')

#Get all balances
all_balance = bit.get_balances()["result"]

#Start counter
total = 0
for each in all_balance:
    #Check for any value
    currency_available = each["Balance"]["Available"]
    if currency_available > 0:
        #Bitcoin is seperated
        if each["Currency"]["Currency"] == "BTC":
            total += currency_available
        #All other value converted to BTC
        else:
            coin_btc_value =  each["BitcoinMarket"]["Last"]
            btc_count = coin_btc_value*currency_available
            total += btc_count

#Website

start_amount = 0.01268267
perc_change = (total - start_amount) / start_amount * 100
print "Content-type: text/html\n\n"


head = open("head.html", "r")
print head.read()

print "<p class=\"returns\">Percent Change: %f</p>" % perc_change

close = open("close.html", "r")
print close.read()
