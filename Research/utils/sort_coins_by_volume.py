from Packages.Data import helper as data_helper
import pandas as pd

#what is the time in question
start_time = 1515537707479
how_many_coins = 20
#input into query
data_types = ['quote_asset_volume']
end_time = start_time + 60000 - 1
#Prepping db queries
engine,conn = data_helper.instantiate_engine()
coin_df = pd.read_csv('coins.csv')
out_list = []
for coin in coin_df.values:
    coin = coin[0]
    print('Trying {}'.format(coin))
    try:
        temp_df = data_helper.query_raw_data(coin,data_types,start_time,end_time,conn,normalize=False)
        out_list.append({'coin': coin, 'volume': float(temp_df.values[0][0])})
    except Exception as e:
        print(e)
volume_df = pd.DataFrame(out_list)
volume_df = volume_df.sort_values('volume', ascending=False)
print(volume_df.head(how_many_coins).coin.values)