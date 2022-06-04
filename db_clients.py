import pyodbc
import pandas as pd
from datetime import datetime

connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                                'Server=172.22.1.82;'
                                'Database=QT_2;'
                                'CHARSET=UTF8;'
                                'uid=wss_price;pwd=HzlRt4$$axzG-*UlpuL2gYDu')


def get_product(num_prod):
    query = "SELECT top({}) ID,Name,CategoryID,Company FROM PRODUCT ".format(num_prod)
    df = pd.read_sql(query,con=connection)
    return df

def get_company(id_product):
    query = "SELECT Company FROM PRODUCT where ID = {} ".format(id_product)
    df = pd.read_sql(query,con=connection)

    return df.loc[0,'Company']
def get_latest_product(num_prod):
    query = "SELECT top({}) ID,Name,CategoryID,Company FROM PRODUCT  WITH (NOLOCK) where Valid = 1 order by ID DESC".format(num_prod)
    df = pd.read_sql(query,con=connection)
    return df
def get_name_product(id_product):
    query = "SELECT ID,Name,CategoryID,Company FROM PRODUCT  where ID = {} ".format(id_product)
    df = pd.read_sql(query,con=connection)
    return df
# def get_product_by_date(s,e):
#     query = "SELECT ID,Name,CategoryID,Company FROM PRODUCT where LastUpdate > CURRENT_TIMESTAMP - {0} and LastUpdate < CURRENT_TIMESTAMP - {1}".format(s,e)
#     df = pd.read_sql(query,con=connection)
#     return df

if __name__ == "__main__":
    df = get_latest_product(10)
    print(df)