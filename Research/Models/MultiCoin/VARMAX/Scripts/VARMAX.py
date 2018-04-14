__author__ = 'Ian', 'Joel'


import statsmodels as sm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from statsmodels.tsa.api import VAR
from Data.Scripts.data import data

type = 'Hourly'
X_train, Y_train = data.import_data(set= 'train', type= 'Hourly')

set = 'train'
X_test,Y_test = data.import_data(set= set,  type= 'Hourly')

VAR_model = VAR(X_train.values)

results = VAR_model.fit(1)

# initialize predict on test set
predictions_test = np.zeros((X_test.shape[0],X_test.shape[1]))
predictions_test_stress = np.zeros((X_test.shape[0],X_test.shape[1]))

# turn into numpy array
X_test_matrix = X_test.values

# predict one-step ahead out-of-sample
for i in range(0,X_test.shape[0]):
    predictions_test[i] = results.forecast(X_test_matrix[i,:].reshape(1,20), steps=1)

# Turn back into panda data frame and save to csv
Test_pred = pd.DataFrame(data=predictions_test, index=X_test.index, columns=X_test.columns)

# Drop columns that are not returns
for column in Test_pred.columns:

    if column.split('_')[0] != 'return':

        Test_pred.drop(column, 1, inplace=True)

Test_pred.to_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
                 + '/Pred_CSVs/VARMAX_{}_{}.csv'.format(set, type))

# pred = np.where(Test_pred.values > 0, 1, 0)
#
# sums = np.sum(pred, axis= 1)
#
# sums = np.clip(sums, 1, pred.shape[1])
#
# sums = np.reshape(sums, (sums.shape[0], 1))
#
# pred = pred / sums
#
# print('Rough Return: {}'.format(np.prod(np.sum(pred * Y_test.values, axis = 1) + 1)))