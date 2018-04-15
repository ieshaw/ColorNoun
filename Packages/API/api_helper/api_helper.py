import json

def retreive_key(json_path, key_name, public= 'key', private= 'secret'):

	'''
	This is a helper function to import api keys from JSON's that hold dictionaries of the form
	{key_name:{public: 'public_key', private: 'private_key'}}

	param json_path: local path to json holding api keys
	param key_name: name of desired key within json
	param public: the dictionary key refering to the public api key
	param private: the dictionary key refering to the private api key
	'''

    with open(json_path) as secrets_file:
        secrets = json.load(secrets_file)
        secrets_file.close()

    return secrets[key_name][public], secrets[key_name][private]