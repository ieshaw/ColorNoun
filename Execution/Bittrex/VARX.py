from Packages.API.Bittrex.bittrex import Bittrex
from Packages.API.Bittrex import helper
import pandas as pd
from statsmodels.tsa.api import VAR

def train_run_VAR(X_df):
    '''
    :param X_df: recent hourly data from
    :return: one line datatframe of predictions for returns of next dataframe
    '''
    VAR_model = VAR(X_df.values)
    results = VAR_model.fit(1)
    prediction = results.forecast(X_df.values[-1, :].reshape(1, 20), steps=1)
    pred_df = pd.DataFrame(data=prediction, columns=X_df.columns)
    # Drop columns that are not returns
    for column in pred_df.columns:
        if column.split('_')[0] != 'return':
            pred_df.drop(column, 1, inplace=True)
    return pred_df

def preds_to_weights(pred_df):
    '''
    :param pred_df: data fream of columns 'return_Ticker'
    :return: one row dictionary of expected returns for next hour
    '''
    pred_df = pred_df.where(pred_df > 0, 0)
    sum = float((pred_df.sum(axis = 1)).values)
    out = {}
    for column in pred_df.columns:
        coin = column.split('_')[1]
        out[coin] = float(pred_df[column].values)/ sum
    return out

key_json_path = '.exchange_keys.json'
key_name = 'bittrex_beta_ro'
bit1, bit2 = helper.instantiate_bittrex_objects(key_name, key_json_path)
X_df = helper.get_recent_data(bit2, coins = ['ETH', 'XRP', 'LTC', 'NEOS', 'ADA'], freq = 'hour')
pred_df = train_run_VAR(X_df)
weights_dict = preds_to_weights(pred_df)
print(weights_dict)
print(helper.trade_on_weights(weights_dict,bit1))