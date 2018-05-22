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
stmt = 'SELECT * from binance_historic_data_raw WHERE open_time > 1500063360000'
df = pd.read_sql(stmt, conn)