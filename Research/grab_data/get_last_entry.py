import pandas as pd
from sqlalchemy import create_engine, select

#Connecting to mysql by providing a sqlachemy engine
engine_string = 'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST_IP}:{MYSQL_PORT}/{MYSQL_DATABASE}'
engine = create_engine(engine_string.format(MYSQL_USER = "bill",
                                            MYSQL_PASSWORD = "thegoat16",
                                            MYSQL_HOST_IP = "colornoundb.cslnpupmbbxh.us-east-1.rds.amazonaws.com",
                                            MYSQL_PORT = "3306",
                                            MYSQL_DATABASE = "colornoundb"),
                        echo=False)

conn = engine.connect()
coin = 'ETH'
stmt = '''SELECT open_time from binance_historic_data_raw WHERE coin='{}' ORDER BY open_time DESC LIMIT 1'''.format(coin)
last_epoch = pd.read_sql(stmt, conn).values[0][0]