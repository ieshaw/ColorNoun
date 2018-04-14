__author__ = 'Ian'

import requests
import datetime
import os
import pandas as pd

def get_polo_data()
url = https://poloniex.com/public?command=returnChartData&currencyPair=BTC_ETH&start=1435699200&end=9999999999&period=14400
page = requests.get(url)
data = page.json()['Data']
df = pd.DataFrame(data)