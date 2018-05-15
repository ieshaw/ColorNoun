from Packages.API.General.helper import key_retriever, get_portfolio_val_BTC, \
    instantiate_api_object, get_exchange_df, send_email

def fund_val_BTC(key_list, key_path):
    fund_val = 0
    for key_name in key_list:
        key_status = 'ro'
        exchange, public_key, private_key = key_retriever(key_path, key_name, key_status)
        fund_val += get_portfolio_val_BTC(exchange, public_key, private_key)
    return fund_val

def generate_fund_return_str(fund_name, key_list, key_path, orig_BTC,
                             orig_USD, curr_BTC_val_USD):
    curr_BTC = fund_val_BTC(key_list, key_path)
    curr_USD = curr_BTC * curr_BTC_val_USD
    returns_BTC = (curr_BTC/orig_BTC) - 1
    returns_USD = (curr_USD/orig_USD) - 1
    fund_str = "{} Fund. Return USD: {:.2f}%. Return BTC: {:.2f}%.".format(fund_name,
        100 * returns_USD, 100 * returns_BTC)
    return fund_str

#load in API keys
key_path = '.exchange_keys.json'
exchange, public_key, private_key = key_retriever(key_path,key_name='Binance_Alpha',
                                                  status='ro')
api_object = instantiate_api_object(exchange,public_key,private_key)
exchange_df = get_exchange_df(exchange,api_object)
BTC_val_USD = exchange_df.loc[exchange_df.market == 'BTCUSDT', 'price'].values[0]
#identify which keys belong to which funde
large_cap_key = ['Bittrex_Beta_Large']
alpha_keys_bit = ['Bittrex_Alpha']
alpha_keys_bin = ['Binance_Alpha']
#find beta health
beta_str = generate_fund_return_str(fund_name='Large Cap Index', key_list= large_cap_key,
                               key_path=key_path, orig_BTC=0.38536886, orig_USD=3626,
                               curr_BTC_val_USD= BTC_val_USD)
#find alpha health
alpha_str_bin = generate_fund_return_str(fund_name='Arbitrage_Bin', key_list= alpha_keys_bin,
                               key_path=key_path, orig_BTC=0.033914920365999995, orig_USD=291.9759234753196,
                               curr_BTC_val_USD= BTC_val_USD)
alpha_str_bit = generate_fund_return_str(fund_name='Arbitrage_Bit', key_list= alpha_keys_bit,
                               key_path=key_path, orig_BTC=0.0322482994705332, orig_USD=277.6278675227832,
                               curr_BTC_val_USD= BTC_val_USD)
#send email notifying about health
send_email(alpha_str_bin + '\n' + alpha_str_bit + '\n' + beta_str, subj='Fund Health')
# print(alpha_str_bin + '\n' + alpha_str_bit + '\n' + beta_str)