__author__ = 'Ian'

import pandas as pd
import os

ratios = {'train': 0.7, 'dev': 0.85}

full_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '/CSVs/Processed/Polo/'

x_df = pd.read_csv(full_dir + 'X.csv',index_col=0)

y_df = pd.read_csv(full_dir + 'Y.csv',index_col=0)

#y doesnt have the last index that x does

x_df = x_df.drop(x_df.last_valid_index())

index_dict = {}

index_dict['train'] = x_df.iloc[0:int(ratios['train']*len(x_df))].index

index_dict['dev'] = x_df.iloc[int(ratios['train']*len(x_df)): int(ratios['dev']*len(x_df))].index

index_dict['test'] = x_df.iloc[int(ratios['dev']*len(x_df)):].index


for key in index_dict:

    output_dir = full_dir + '/{}'.format(key)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    x_df.loc[index_dict[key]].to_csv('{}/x.csv'.format(output_dir))

    y_df.loc[index_dict[key]].to_csv('{}/y.csv'.format(output_dir))


