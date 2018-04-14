__author__ = 'Ian'

#using https://gist.github.com/spro/ef26915065225df65c1187562eca7ec4

import os

import numpy as np
import pandas as pd
import torch
from Models.MultiCoin.R2N2.Scripts.RNN import RNN
from torch.autograd import Variable

from Data.Scripts.data import data

torch.manual_seed(1)

def load_data(set = 'dev'):

    #import data
    X,Y = data.import_data(set= set)

    ar_returns = pd.read_csv(os.path.abspath(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), '..'))
                             + '/VARMAX/Pred_CSVs/VARMAX_{}.csv'.format(set), index_col=0)

    X = X.loc[ar_returns.index]
    residual_df = X.copy()

    for column in residual_df.columns:

        if column.split('_')[0] != 'return':
            residual_df.drop(column, 1, inplace=True)

        else:
            residual_df[column] = residual_df[column] - ar_returns[column]
            Y[column] = Y[column] - ar_returns[column]

    X = X.join(residual_df, how = 'inner', rsuffix = 'residual')

    Y = Y.dropna()
    X = X.loc[Y.index]

    x = X.as_matrix()
    y = Y.as_matrix()

    return x,y,X,Y, ar_returns

set = 'dev'
hidden_size = 10
model_string = 'VAR_LSTM_1_BFC_1_AFC_1_Act_None'
model_name = '{}_H{}'.format(model_string, hidden_size)

model_params_file_str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) \
                        + '/model_params/{}.pth.tar'.format(model_name)

x,y,X,Y, ar_returns = load_data(set= set)

# set model
model = RNN(hidden_size=hidden_size, input_size=len(X.iloc[0:1].values[0]), output_size=len(Y.iloc[0:1].values[0]))
model.load_state_dict(torch.load(model_params_file_str))

y_pred = np.zeros(shape=y.shape)

for iter in range(len(x)):
    input = Variable(torch.from_numpy(x[iter]).float())

    output = model.forward(input)

    y_pred[iter] = output.data.numpy()

Y_pred = pd.DataFrame(data=y_pred + ar_returns.as_matrix(), index=Y.index, columns=Y.columns)

Y_pred.to_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
              + '/Pred_CSVs/{}_{}.csv'.format(model_string,set))