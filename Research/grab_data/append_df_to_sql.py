from sqlalchemy import create_engine
import pandas as pd

def append_transactions(data, table, index, engine):
    try:
        data.to_sql(table, con=engine, index=True, index_label=index, if_exists='append')
        return 'Success'
    except Exception as e:
        print("Initial failure to append: {}\n".format(e))
        print("Attempting to rectify...")
        existing = pd.read_sql(table, con=engine)
        mask = ~data[index].isin(existing[index])
        to_insert = data.loc[mask]
        try:
            to_insert.to_sql(table, con=engine, index=False, if_exists='append')
            print("Successful deduplication.")
        except Exception as e2:
            "Could not rectify duplicate entries. \n{}".format(e2)
        return 'Success after dedupe'


#Connecting to mysql by providing a sqlachemy engine
engine_string = 'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST_IP}:{MYSQL_PORT}/{MYSQL_DATABASE}'
engine = create_engine(engine_string.format(MYSQL_USER = "Zayne",
                                            MYSQL_PASSWORD = "(1Color1)",
                                            MYSQL_HOST_IP = "colornoun-fund-details.cpzjvssiijud.us-west-1.rds.amazonaws.com",
                                            MYSQL_PORT = "3306",
                                            MYSQL_DATABASE = "Historical_Data"),
                        echo=False)