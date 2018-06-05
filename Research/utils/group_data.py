import pandas as pd
import numpy as np

def group_returns(input_filename, output_filename, num_steps_grouped):
    ## Manipulate DataFrame
    data_df = pd.read_csv(input_filename)
    out_cols = data_df.columns
    # create keys to group bby
    data_df['row_num'] = 1
    data_df['row_num'] = ((data_df['row_num'].cumsum() - 1) / num_steps_grouped).apply(np.floor).astype(int)
    return_cols = [col for col in data_df.columns if col.split('_')[0] == 'return']
    data_df[return_cols] += 1
    grouped_df = data_df.groupby('row_num')
    filt_df = pd.DataFrame(columns=out_cols)
    filt_df['open_time'] = grouped_df['open_time'].first()
    filt_df[return_cols] = grouped_df[return_cols].prod() - 1
    # save to csv
    filt_df.to_csv(output_filename, index=False)

#Inputs
input_filename = 'test_csvs/test_1m.csv'
num_steps_grouped = 15
name_min_dict = {
    '15m' : 15,
    '30m': 30,
    '1h': 60,
    '2h': 120,
    '6h': 60*6,
    '12h': 12*60,
    '1d': 24*60
}
for key in name_min_dict:
    output_filename = 'dev_csvs/train_{}.csv'.format(key)
    print('On {}'.format(key))
    group_returns(input_filename, output_filename, num_steps_grouped=name_min_dict[key])