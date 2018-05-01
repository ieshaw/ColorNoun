
"""
Code to simply initialize api across all code and organize all keys used in one place
"""

def key_retriever(json_path, key):
	import json
	import os
	with open(json_path) as secrets_file:
		secrets = json.load(secrets_file)
		secrets_file.close()
	return secrets[key]['key'], secrets[key]['secret']

def send_text(msg):
	from twilio.rest import Client
	
	# the following line needs your Twilio Account SID and Auth Token
	client = Client("ACd4126bcd31db83c4cef178d7acef406e", 
		"01cdd13084823d02e86699442d20be3a")
	
	# change the "from_" number to your Twilio number and the "to" number
	# to the phone number you signed up for Twilio with, or upgrade your
	# account to send SMS to any phone number
	client.messages.create(to="+19518521157", 
			       from_="+17608915341", 
			       body="Rebalancing Index Fund")
