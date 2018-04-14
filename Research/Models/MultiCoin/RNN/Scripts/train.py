__author__ = 'Ian'

#using https://gist.github.com/spro/ef26915065225df65c1187562eca7ec4

import os
import time

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from Models.MultiCoin.RNN.Scripts.RNN import RNN
from statsmodels.tsa.api import VAR
from torch.autograd import Variable

from Data.Scripts.data import data

torch.manual_seed(1)

X,Y = data.import_data(set= 'train')
x = X.as_matrix()
y = Y.as_matrix()
#hyperparameters
hidden_size = 10
n_epochs = 230
model_string = 'LSTM_1_BFC_1_AFC_1_Act_None'
optim_string = 'Adam'
model_name = '{}_H{}'.format(model_string, hidden_size)

#set
input_size = len(X.iloc[0:1].values[0])
output_size = len(Y.iloc[0:1].values[0])

#set model, loss, and optimization
model = RNN(hidden_size= hidden_size, input_size= input_size, output_size= output_size)
#load in model if want to continue training
# model.load_state_dict(torch.load(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
#                    + '/model_params/{}.pth.tar'.format(model_name)))

criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters())


#train model
losses = np.zeros(n_epochs) # For plotting
best_loss = np.inf
time_train = time.time()

for epoch in range(n_epochs):

    tic = time.time()

    for iter in range(len(x)):
        input = Variable(torch.from_numpy(x[iter]).float())
        target = Variable(torch.from_numpy(y[iter]).float())

        output = model.forward(input)

        optimizer.zero_grad()
        loss = criterion(output, target)
        loss.backward(retain_graph=True)
        optimizer.step()

        losses[epoch] += loss.data[0]

    print(epoch, losses[epoch])
    print('Time of epoch: {}'.format(time.time() - tic))

    if losses[epoch] < best_loss:

        best_loss = losses[epoch]

        # Save losses to csv

        loss_df = pd.DataFrame({'loss': losses[:(epoch + 1)] / len(x)})
        loss_df.to_csv(
            os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '/loss_csvs/{}.csv'.format(model_name))

        # Save weights
        torch.save(model.state_dict(), os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
                   + '/model_params/{}.pth.tar'.format(model_name))

        filename = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "/records/{}.txt".format(model_name)
        with open(filename, 'w') as f:
            f.write("{} \n".format(model_string))
            f.write("{} \n".format(model_name))
            f.write("Num_Epochs = {}\n".format(epoch + 1))
            f.write("Hidden_Size = {}\n".format(hidden_size))
            f.write("Optimizer = {}\n".format(optim_string))
            f.write("Loss = {}\n".format(best_loss))
            f.write("Time spent = {0}\n".format(time.time() - time_train))

