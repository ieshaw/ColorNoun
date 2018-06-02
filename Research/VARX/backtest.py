import pandas as pd
from statsmodels.tsa.api import VAR
import matplotlib.pyplot as plt

def run_VARX_backtest(train_filename,dev_filename,plot_title):
    #load in data
    train_df = pd.read_csv(train_filename, index_col=0)
    #load in testing data
    dev_df = pd.read_csv(dev_filename, index_col=0)
    #Create VAR Model
    model = VAR(train_df.values)
    results = model.fit(maxlags=30, ic='aic')
    #loop through to get the predictions
    lag_order = results.k_ar
    print('Lag Order: {}'.format(lag_order))
    if lag_order <= 0:
        print('No good VAR.')
        return 0
    pred_df = dev_df[lag_order:].copy()
    true_df = dev_df[lag_order:].copy()
    for i in range(lag_order, len(dev_df)):
        pred_df.iloc[i-lag_order] = results.forecast(dev_df[(i-lag_order):i].values, steps=1)
    #only care about return columns
    return_cols = []
    for col in pred_df.columns:
        if col.split('_')[0] == 'return':
            return_cols.append(col)
    pred_df = pred_df[return_cols].copy()
    true_df = true_df[return_cols].copy()
    #only invest if positive predicted returns
    pred_df.where(pred_df > 0, 0, inplace = True)
    #resize expected returns to portfolio weightings
    weights_df = pred_df.divide(pred_df.sum(axis=1), axis='index')
    weights_df.fillna(0, inplace=True)
    #execute backtest
    back_df = weights_df.multiply(true_df)
    #subtract off roundrtip transaction costs
    back_df = back_df - weights_df.where(weights_df == 0, 1) * 0.005
    #get the returns by timestep
    return_series = back_df.sum(axis=1)
    #create the portfolio series
    portfolio_series = (return_series + 1).cumprod()
    #plot the results
    portfolio_series.plot()
    plt.title(plot_title)
    plt.show()

freq_list = ['1m','6h', '15m', '12h', '30m', '1h', '2h', '1d']
for freq in freq_list:
    print('On {}'.format(freq))
    filename = 'data_csvs/train_{}.csv'.format(freq)
    solution_not_found = True
    while solution_not_found:
        try:
            run_VARX_backtest(train_filename=filename, dev_filename=filename, plot_title=freq)
            solution_not_found = False
        except Exception as e:
            print(e)