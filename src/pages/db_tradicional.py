import streamlit as st
import pandas as pd

from src.config import config
from src.database import queries
from src.database.mysql import MysqlDB



def data_setup():
    db = MysqlDB()
    db.connection(user=config.MYSQL_USER, password=config.MYSQL_PASSWORD, 
                host=config.MYSQL_HOST, port=config.MYSQL_PORT, 
                database=config.MYSQL_DATABASE)

    return db
    

def write():
    db = data_setup()
    
    q1 = db.select(queries.QUERY1)
    df = pd.DataFrame(q1, columns=['nome_credor', 'media_liquida_semestral'], index=[i for i in range(1, 51)])

    q2 = db.select(queries.QUERY2)
    df2 = pd.DataFrame(q2, columns=['trimestre', 'codigo_acao', 'nome_acao', 'valor_empenhado_total', 'ano'])

    q3 = db.select(queries.QUERY3)
    df3 = pd.DataFrame(q3, columns=['mes_movimentacao', 'quantidade_pagamentos', 'total_pagamentos'])

    q4 = db.select(queries.QUERY4)
    df4 = pd.DataFrame(q4, columns=['quadrimestre', 'nome_acao', 'quantidade_creditos', 'media_valor_liquido_acao'])


    with st.spinner("Loding..."):
        st.write(
            """
            # Despesas Orçamentárias - Banco Tradicional
            """
        )
        st.divider()
        st.dataframe(
            df,
            column_config={
        "nome_credor": "Nome do credor",
        "media_liquida_semestral": "Média líquida semestral"})