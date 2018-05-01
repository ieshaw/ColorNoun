from Packages.API.Bittrex import helper

key_json_path = '.exchange_keys.json'
key_name = 'bittrex_ro'
bit1, bit2 = helper.instantiate_bittrex_objects(key_name, key_json_path)
print("Portfolio Size in BTC: {}".format(helper.get_portfolio_worth_in_BTC(bit1)))