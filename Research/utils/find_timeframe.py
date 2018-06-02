import numpy as np
import pandas as pd
import time

def find_sample_period(coins,num_days,start_limit,end_limit):
    if end_limit == 0:
        end_limit = int(time.time() * 1e3)
    # load in the data
    start_times = []
    start_time_df = pd.read_csv('first_epoch.csv')
    missing_df = pd.DataFrame()
    for coin in coins:
        start_times.append(start_time_df.loc[start_time_df['coin'] == coin]['first_epoch'].values[0])
        missing_df = missing_df.append(pd.read_csv('missing_epochs/{}.csv'.format(coin)), ignore_index=True)
    # Establish the Start of the window
    latest_start = max(max(start_times), start_limit)
    print(latest_start)
    missing_df = missing_df.loc[missing_df['start'] > latest_start].copy()
    # Start the Algotihm
    temp_df = pd.DataFrame()
    temp_df['epoch'] = missing_df['start'].copy()
    temp_df['flag'] = -1
    a_df = pd.DataFrame()
    a_df['epoch'] = missing_df['end'].copy()
    a_df['flag'] = 1
    temp_df = temp_df.append(a_df, ignore_index=True)
    temp_df.sort_values('epoch', ascending=True, inplace=True)
    temp_df['sum_prev'] = temp_df.flag + temp_df.flag.shift(1)
    temp_df['sum_aft'] = temp_df.flag + temp_df.flag.shift(-1)
    temp_df.fillna(0, inplace=True)
    temp_df = temp_df.loc[(temp_df['sum_prev'] != 2) & (temp_df['sum_aft'] != -2)][['epoch', 'flag']].copy()
    temp_df = temp_df.append(pd.DataFrame([{'epoch': latest_start, 'flag': 1}, {'epoch': end_limit, 'flag': -1}]),
                             ignore_index=True)
    temp_df.sort_values('epoch', ascending=True, inplace=True)
    synth_tl = pd.concat([temp_df.loc[temp_df['flag'] == 1]['epoch'].reset_index(drop=True).astype(int).rename('start'),
                          temp_df.loc[temp_df['flag'] == -1]['epoch'].reset_index(drop=True).astype(
                              int).rename('end')]
                         , axis=1)
    synth_tl.eval('length = end - start', inplace=True)
    # convert the lenght from milliseconds to days
    ms_in_day = 1000 * 60 * 24 * 60
    synth_tl['length'] /= ms_in_day
    # only consider windows where continous amount of days desired
    synth_tl['length'] -= num_days
    synth_tl['length'].where(synth_tl['length'] > 0, 0, inplace=True)
    # take the cumulatice sum
    synth_tl['running_sum'] = synth_tl['length'].cumsum()
    # choose a random start point
    start_day = np.random.randint(0, synth_tl['length'].sum())
    query_df = synth_tl.loc[synth_tl['running_sum'] > start_day].copy()
    start_time = (query_df['start'].values[0]) + ((start_day - query_df['running_sum'].values[0]) * ms_in_day)
    end_time = start_time + num_days * ms_in_day
    print('A random {} day window of data availability'.format(num_days))
    print('Start Epoch: {}'.format(int(start_time)))
    print('End Epoch: {}'.format(int(end_time)))

coins = ['TRX', 'ETH', 'XRP', 'LUN', 'ICX', 'ADA', 'EOS', 'XVG', 'NEBL',
       'OMG', 'ELF', 'BCPT', 'APPC', 'LRC', 'NEO', 'FUN', 'QTUM', 'LTC',
       'BNB', 'VEN']
num_days = 30
#put 0 if no preference
start_limit = 1515537707479
#put 0 is no preference
end_limit = 0
#run the algorithm
find_sample_period(coins,num_days,start_limit,end_limit)