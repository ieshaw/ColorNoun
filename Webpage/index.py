#!/home/tridxmod/mypython/bin/python

def html_table(alist,sublen,title):
    print '<table align=\"center\">'
    #Print title
    print "<thead>"
    print '  <tr><th style="background-color:#666;color:#FFF;", colspan = %d> %s </th> </tr>' % (sublen,title)
    #Print Colum Headings
    print '  <tr><th>'
    print '    </th><th>'.join(alist[0])
    print '  </th></tr>'
    print '</thead>'

    for sublist in alist[1:]:
        print '  <tr><td>'
        print '    </td><td>'.join(sublist)
        print '  </td></tr>'
    print '</table>'



from bittrex import Bittrex
#Load API
api_key = 'c2402b7f906b4d82b97ca0561d4725ba'
secret_key = '0bfb77b4b204453eba27c95f2e124e91'
bit = Bittrex(api_key=api_key, api_secret=secret_key, api_version='v2.0')

#Get all balances
all_balance = bit.get_balances()["result"]

#Get current Bitcoin Value
btc_price = bit.get_btc_price()["result"]["bpi"]["USD"]["rate_float"]

#Start counter and holdings
holdings = [["Coin", "Available", "BTC Value", "USD Value"]]
total = 0

#Get holdings and value
for each in all_balance:
    #Check for any value
    currency_available = each["Balance"]["Available"]
    if currency_available > 0:
        #Bitcoin is seperated
        if each["Currency"]["Currency"] == "BTC":
            btc_count = currency_available
            total += currency_available
        #All other value converted to BTC
        else:
            coin_btc_value =  each["BitcoinMarket"]["Last"]
            btc_count = coin_btc_value*currency_available
            total += btc_count
        usd_value = btc_count * btc_price
        # Add new holding instance
        holdings.append([each["Currency"]["Currency"],str(currency_available),str(btc_count),str(usd_value)])

#Get order history and disposits
all_orders =  bit.get_order_history()["result"]
recent_orders = all_orders[:10]
history = [["Market", "Time", "Type", "Quantity", "USD Value"]]

for order in recent_orders:
    order_value = (order["Quantity"] * order["PricePerUnit"]) * btc_price

    if order["OrderType"] == "LIMIT_BUY":
        order_value = order_value * -1

    history.append([order["Exchange"], str(order["TimeStamp"]),
                     order["OrderType"], str(order["Quantity"]), str(order_value)])


#Get portfolio value
#No Code Yet
portfolios = [["Name","Strategy","BTC Count", "USD Value", "Total Transactions"],
              ["Lazarus","Coin VARMAX", str(total), str(total*btc_price), str(len(all_orders))]]

#Begin Website Code
start_amount = 0.01268267
perc_change = (total - start_amount) / start_amount * 100

#Content Header for cPanel
print "Content-type: text/html\n\n"

#Print Heading of HTML Page
head = open("head.html", "r")
print head.read()

#Begin Body of HTML
print "<h2 >Tridens Capital</h2>"
print "<p class=\"returns\">Percent Change: %f</p>" % perc_change

html_table(portfolios,len(portfolios[0]),"Portfolios")

html_table(holdings,len(holdings[0]),"Current Holdings")

html_table(history,len(history[0]),"Previous Transactions")

#End Body of HTML

#Print Page Close
close = open("close.html", "r")
print close.read()
