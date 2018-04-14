__author__ = 'Ian'

import os
import pandas as pd

class data:

    '''
    A class in order to import data into any backtesting script
    '''

    def import_data(set= 'train', type= 'Polo'):

        '''
        :param set: 'train', 'dev', or 'test'
        :return: data_set, labels. as pandas dataframes
        '''

        x_df = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
                           + '/CSVs/Processed/{}/{}/x.csv'.format(type, set), index_col=0)

        y_df = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
                           + '/CSVs/Processed/{}/{}/y.csv'.format(type, set), index_col=0)

        return x_df, y_df