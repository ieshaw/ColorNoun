import json
import os
"""
Code to simply initialize api across all code and organize all keys used in one place
"""

def key_retriever(json_path, key):

    with open(json_path) as secrets_file:
        secrets = json.load(secrets_file)
        secrets_file.close()

    return secrets[key]['key'], secrets[key]['secret']
