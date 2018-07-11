from Packages.Data import helper as data_helper
import os
import pandas as pd

#desired inputs
# coins = ['TRX', 'ETH', 'XRP', 'LUN', 'ICX', 'ADA', 'EOS', 'XVG', 'NEBL',
#        'OMG', 'ELF', 'BCPT', 'APPC', 'LRC', 'NEO', 'FUN', 'QTUM', 'LTC',
#        'BNB', 'VEN']
coins = ['ADA', 'NEBL', 'BCPT', 'NEO', 'FUN']
data_types = ['return']
start_time = 1519875336383
end_time = 1520480136383
file_name = 'dev'
##Automatic updates to inputs
data_types.append('open_time')
out_dir = os.getcwd() + '/data_csvs'
if not os.path.exists(out_dir):
    os.mkdir(out_dir)
#query data and save file
engine,conn = data_helper.instantiate_engine()
out_df = pd.DataFrame()
for coin in coins:
    print('Grabbing {} Data'.format(coin))
    temp_df = data_helper.query_raw_data(coin,data_types,start_time,end_time,conn)
    temp_df.set_index('open_time', inplace=True)
    #rename the comlumns
    map_dict = {}
    for column in temp_df.columns:
        map_dict[column] = '{}_{}'.format(column, coin)
    temp_df.rename(columns=map_dict, inplace=True)
    #append this to the out_Df
    out_df = out_df.join(temp_df, how='outer')
out_df.to_csv('{}/{}.csv'.format(out_dir,file_name), index=True)