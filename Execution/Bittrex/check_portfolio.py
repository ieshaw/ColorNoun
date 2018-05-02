from Packages.API.Bittrex import helper
from Packages.API.Helper.helper import send_email

def fund_return(bit1,bit2, original_BTC, original_USD, fund_name):
    curr_BTC = helper.get_portfolio_worth_in_BTC(bit1)
    curr_USD = curr_BTC * bit2.get_btc_price()['result']['bpi']['USD']['rate_float']
    returns_BTC = (curr_BTC/original_BTC) - 1
    returns_USD = (curr_USD/original_USD) - 1
    fund_str = "{} Fund. Return USD: {:.2f}%. Return BTC: {:.2f}%.".format(fund_name,
        100 * returns_USD, 100 * returns_BTC)
    return fund_str

key_json_path = '.exchange_keys.json'

key_name = 'bittrex_beta_ro'
bit1, bit2 = helper.instantiate_bittrex_objects(key_name, key_json_path)
beta_original_BTC = 0.38536886
beta_original_USD = 3626
beta_str = fund_return(bit1,bit2,beta_original_BTC,beta_original_USD,'Beta')

key_name = 'bittrex_alpha'
bit1, bit2 = helper.instantiate_bittrex_objects(key_name, key_json_path)
alpha_original_BTC = 0.03503836
alpha_original_USD = 317
alpha_str = fund_return(bit1,bit2,alpha_original_BTC,alpha_original_USD,'Alpha')

#print(alpha_str + '\n' + beta_str)
send_email(alpha_str + '\n' + beta_str, toaddrs=['ian@colornoun.capital'])