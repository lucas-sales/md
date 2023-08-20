import streamlit as st
import pandas as pd
import plotly.express as px

from src.config import config
from src.database import dw_queries
from src.database.mysql import MysqlDB



def data_setup():
    """
    Estabelece a conexão com o banco de dados e retorna o objeto de conexão.
    """
    db = MysqlDB()
    db.connection(
        user=config.MYSQL_USER, 
        password=config.MYSQL_PASSWORD, 
        host=config.MYSQL_HOST, 
        port=config.MYSQL_PORT, 
        database=config.MYSQL_DATABASE_DW
    )
    return db

def fetch_data(db, query, columns):
    """
    Busca os dados usando o objeto de conexão do banco e a consulta fornecida.
    Retorna um DataFrame com as colunas especificadas.
    """
    data = db.select(query)
    return pd.DataFrame(data, columns=columns)

def write():
    # Configura a conexão com o banco de dados
    db = data_setup()
    
    # Carregando dados da QUERY 1
    df1 = fetch_data(db, dw_queries.QUERY1, ['credor', 'ano', 'mes', 'trimestre', 'valor_pago_total',
                                              'valor_liquidado_total', 'diferenca_pago_liquidado'])
    

    with st.spinner("Loding..."):
        st.title(' 🖥 Data Warehouse')
        st.subheader('Gráficos que demonstram o resultado de algumas perguntas feitas ao Data Warehouse, gerado a partir da base '
                     '"_Despesas Orçamentárias de Recife_"')
        st.divider()

        st.title("📊 Gráfico 1")
        st.write("> # 1 -  Calcular os 20 maiores valores pagos e liquidados, bem como a diferença entre os valores para cada "
                 "credor ao longo do tempo:")
        
        # Adicionando um dropdown para escolher o mês:
        mes_selected = st.selectbox('Escolha um mês:', df1['mes'].unique())
        
        # Filtrando o DataFrame com base na seleção:
        df1_filtered = df1[df1['mes'] == mes_selected].head(20)


        #Gerando o gráfico para a pergunta 1:
        fig = px.bar(df1_filtered, x='credor', y=['valor_pago_total', 'diferenca_pago_liquidado'], 
                 labels={
                        'credor' : 'Credor',
                        'variable': 'Valores'
                        },
                 title='Valor Pago e Valor Liquidado por Credor')
        fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
        st.plotly_chart(fig)