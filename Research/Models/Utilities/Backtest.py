__author__ = 'Ian'

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class backtest:

    '''
    A class to backtest models
    '''

    def __init__(self, true_df, pred_df):

        self.true_df = true_df.copy()

        self.pred_df = pred_df.copy()

        self.pred_df.columns = self.true_df.columns

    def run_backtest(self):

        pred = self.pred_df.as_matrix()

        actual = self.true_df.as_matrix()

        pred = np.clip(pred, 0, np.inf)

        pred = np.clip(pred, 0, np.inf)

        sums = np.sum(pred, axis=1)

        sums = np.clip(sums, 0.0001, np.inf)

        sums = np.reshape(sums, (sums.shape[0], 1))

        weights = pred / sums

        returns = np.sum(weights * actual, axis=1) + 1

        self.strat_series = returns.cumprod()

        self.strat_return = np.prod(returns) - 1


    def plot_backtest(self, strat_label = 'strat_label'):

        plt.plot(self.strat_series, label='strat')

        plt.show()

