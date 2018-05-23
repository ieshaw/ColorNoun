import mysql.connector
import pandas as pd
from sqlalchemy import create_engine
import helper as data_helper

eth_df = pd.read_csv('eth.csv')
engine, conn = data_helper.instantiate_engine()
data_helper.upload_binance_historical_data(eth_df,engine)
