from Packages.Data import helper as data_helper
import os
import pandas as pd

#desired inputs
coins = ['LTC', 'NEO', 'BCC']
data_types = ['return']
start_time = 1515537707479
end_time = 1515969707479
file_name = 'in_sample'
##Automatic updates to inputs
data_types.append('open_time')
out_dir = os.getcwd() + '/data_csvs'
if not os.path.exists(out_dir):
    os.mkdir(out_dir)
#query data and save file
engine,conn = data_helper.instantiate_engine()
out_df = pd.DataFrame()
for coin in coins:
    temp_df = data_helper.query_raw_data(coin,data_types,start_time,end_time,conn)
    temp_df.set_index('open_time', inplace=True)
    #rename the comlumns
    map_dict = {}
    for column in temp_df.columns:
        map_dict[column] = '{}_{}'.format(column, coin)
    temp_df.rename(columns=map_dict, inplace=True)
    #append this to the out_Df
    out_df = out_df.join(temp_df, how='outer')
out_df.to_csv('{}/{}.csv'.format(out_dir,file_name), index=False)