import streamlit as st
import pandas as pd

from src.config import config
from src.database import queries
from src.database.mysql import MysqlDB



def data_setup():
    db = MysqlDB()
    db.connection(user=config.MYSQL_USER, password=config.MYSQL_PASSWORD, 
                host=config.MYSQL_HOST, port=config.MYSQL_PORT, 
                database=config.MYSQL_DATABASE_DW)

    return db

def write():
    db = data_setup()
    
    with st.spinner("Loding..."):
        st.write(
            """
            # Despesas Orçamentárias - data warehouse
            """
        )