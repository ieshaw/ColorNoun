__author__ = 'Ian'

import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
from Data.Scripts.data import data

set = 'train'
type = 'Hourly'
_, test_actual = data.import_data(set= set, type= type)

test_pred = pd.read_csv('/Users/ianshaw/Downloads/GitHub/tester/Models/MultiCoin/VARMAX/Pred_CSVs/VARMAX_train_Hourly.csv', index_col= 0)

pred = test_pred.as_matrix()

actual = test_actual.as_matrix()

pred = np.clip(pred, 0, np.inf)

pred = np.clip(pred, 0, np.inf)

sums = np.sum(pred, axis= 1)

sums = np.clip(sums, 0.0001, np.inf)

sums = np.reshape(sums, (sums.shape[0], 1))

weights = pred / sums

returns = np.sum(weights * actual, axis = 1) + 1

strat = returns.cumprod()

plt.plot(strat, label = 'strat')

print('Rough Return: {}'.format(np.prod(returns) - 1))

pred = np.ones(actual.shape)

sums = np.sum(pred, axis= 1)

sums = np.clip(sums, 0.0001, pred.shape[1])

sums = np.reshape(sums, (sums.shape[0], 1))

weights = pred / sums

returns = np.sum(weights * actual, axis = 1) + 1

strat = returns.cumprod()

plt.plot(strat, label = 'base')

print('Rough Baseline: {}'.format(np.prod(np.sum(weights * actual, axis = 1) + 1) - 1))

plt.legend()
plt.show()