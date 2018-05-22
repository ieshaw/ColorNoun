import mysql.connector
import pandas as pd
from sqlalchemy import create_engine

def append_df_to_db(df, table_name, engine):
    try:
        df.to_sql(table_name, con=engine, index=False, if_exists='append')
    except Exception as e:
        print(e)

eth_df = pd.read_csv('eth.csv').head(n=25000)

#Connecting to mysql by providing a sqlachemy engine
engine_string = 'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST_IP}:{MYSQL_PORT}/{MYSQL_DATABASE}'
engine = create_engine(engine_string.format(MYSQL_USER = "bill",
                                            MYSQL_PASSWORD = "thegoat16",
                                            MYSQL_HOST_IP = "colornoundb.cslnpupmbbxh.us-east-1.rds.amazonaws.com",
                                            MYSQL_PORT = "3306",
                                            MYSQL_DATABASE = "colornoundb"),
                        echo=False)

table_name='binance_historic_data_raw'
append_df_to_db(eth_df,table_name,engine)