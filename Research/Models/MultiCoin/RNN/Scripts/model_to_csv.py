__author__ = 'Ian'

#using https://gist.github.com/spro/ef26915065225df65c1187562eca7ec4

import os

import numpy as np
import pandas as pd
import torch
from Models.MultiCoin.RNN.Scripts.RNN import RNN
from torch.autograd import Variable

from Data.Scripts.data import data

torch.manual_seed(1)

set = 'dev'
hidden_size = 10
model_string = 'LSTM_1_BFC_1_AFC_1_Act_None'
model_name = '{}_H{}'.format(model_string, hidden_size)

X,Y = data.import_data(set= set)
x = X.as_matrix()
y = Y.as_matrix()

model_params_file_str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) \
                        + '/model_params/{}.pth.tar'.format(model_name)

# set model
model = RNN(hidden_size=hidden_size, input_size=len(X.iloc[0:1].values[0]), output_size=len(Y.iloc[0:1].values[0]))
model.load_state_dict(torch.load(model_params_file_str))

y_pred = np.zeros(shape=y.shape)

for iter in range(len(x)):
    input = Variable(torch.from_numpy(x[iter]).float())

    output = model.forward(input)

    y_pred[iter] = output.data.numpy()

Y_pred = pd.DataFrame(data=y_pred , index=Y.index, columns=Y.columns)

Y_pred.to_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
              + '/Pred_CSVs/{}_{}.csv'.format(model_string,set))