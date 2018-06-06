from Packages.Data import helper as data_helper
from Packages.API.General.helper import key_retriever, trade_on_weights, send_email
from statsmodels.tsa.api import VAR
import numpy as np
import pandas as pd
import time

def group_returns(input_df, num_steps_grouped):
    ## Manipulate DataFrame
    data_df = input_df.copy()
    out_cols = data_df.columns
    # create keys to group bby
    data_df['row_num'] = 1
    data_df['row_num'] = ((data_df['row_num'].cumsum() - 1) / num_steps_grouped).apply(np.floor).astype(int)
    return_cols = [col for col in data_df.columns if col.split('_')[0] == 'return']
    data_df[return_cols] += 1
    grouped_df = data_df.groupby('row_num')
    filt_df = pd.DataFrame(columns=out_cols)
    filt_df[return_cols] = grouped_df[return_cols].prod() - 1
    return filt_df

current_epoch = int(time.time() * 1e3)
coins = ['ADA', 'NEBL', 'BCPT', 'NEO', 'FUN']
data_types = ['return']
ms_in_day = 1000 * 60 * 24 * 60
month_ago = current_epoch - 7 * ms_in_day
train_df = data_helper.grab_data(coins, start_epoch=month_ago, end_epoch=current_epoch, data_list=data_types)
train_df.dropna(inplace=True)
two_hour_df = group_returns(train_df,120).dropna()
try:
    # Create VAR Model
    model = VAR(two_hour_df.values)
    results = model.fit(maxlags=30, ic='aic')
    lag_order = results.k_ar
    #Make Predictions
    pred_array = results.forecast(two_hour_df[-lag_order:].values, steps=1)
    #only consider predictions above roundtrip transaction costs
    weight_array = np.where(pred_array > 0.005, pred_array, 0)
    weight_dict =dict(zip(coins,weight_array.tolist()[0]))
except:
    #if it doesnt work, just have all in BTC
    weight_dict =dict(zip(coins,np.zeros(len(coins))))
##Run Trades
key_path = '.exchange_keys.json'
key_name = 'Binance_Alpha'
key_status = 'live'
exchange, public_key, private_key = key_retriever(key_path,key_name,key_status)
trade_df = trade_on_weights(exchange, public_key, private_key, weight_dict, min_BTC_prop=0.5)
send_email('Running VAR. \n\n Trade Plan. \n\n {}'.format(trade_df),
            subj='VAR', toaddrs=['ian@colornoun.capital'])