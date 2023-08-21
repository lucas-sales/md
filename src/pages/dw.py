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

#Função utilizada para a criação do gráfico da segunda questão
def grafico2(data):
    fig = px.pie(data, names='Modalidade Nome', values='Valor Total',
        title='Distribuição de Gastos por Modalidade de Licitação')
    st.plotly_chart(fig)

def grafico3(data):
    pass

        
def write():
    # Configura a conexão com o banco de dados
    db = data_setup()
    
    # Carregando dados da QUERY 1
    df1 = fetch_data(db, dw_queries.QUERY1, ['credor', 'ano', 'mes', 'trimestre', 'Valor Pago Total',
                                              'Valor Liquidado Total', 'Diferença Pago Liquidado'])

    # Carregando dados da QUERY 2
    df2_trimestre = fetch_data(db, dw_queries.QUERY2, ['Modalidade Nome', 'Trimestre', 'Valor Total'])
    df2_ano = fetch_data(db, dw_queries.QUERY3, ['Modalidade Nome', 'Valor Total'])

    # CArregando dados da QUERY 4
    # df4 = fetch_data(db, dw_queries.QUERY4, ['Mês', 'quantidade de pag.', 'total pag.'])
    

    with st.spinner("Loding..."):
        st.title(' 🖥 Data Warehouse')
        st.subheader('Gráficos que demonstram o resultado de algumas perguntas feitas ao Data Warehouse, gerado a partir da base '
                     '"_Despesas Orçamentárias de Recife_"')
        st.divider()

        st.title("📊 Gráfico 1")
        st.write("> # 1 -  Calcular os 20 maiores valores pagos e liquidados, bem como a diferença entre os valores para cada "
                 "credor ao longo do tempo:")
        st.write("#### ```Utilize o dropdown para selecionar o mês, e ter acesso "
                 "aos valores gastos por cada Credor no respectivo mês.```")
        
        st.write("### ```Clique na legenda abaixo para remover do gráfico```")
        
        # Adicionando um dropdown para escolher o mês:
        mes_selected = st.selectbox('Escolha um mês:', df1['mes'].unique())
        
        # Filtrando o DataFrame com base na seleção:
        df1_filtered = df1[df1['mes'] == mes_selected].head(20)


        #Gerando o gráfico para a pergunta 1:
        fig1 = px.bar(df1_filtered, x='credor', y=['Valor Pago Total', 'Diferença Pago Liquidado'], 
                 labels={
                        'credor' : 'Credor',
                        'variable': 'Valores'
                        },
                 title='Valor Pago e Valor Liquidado por Credor')
        fig1.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
        st.plotly_chart(fig1)

        st.divider()

        st.title("📊 Gráfico 2")
        st.write("> # 2 - Qual a porcentagem de gastos totais gerados por cada modalidade de licitação?")
        st.write("#### ```Utilize o dropdown para selecionar o trimestre, e ter acesso a todos"
                 "aos valores gastos por cada forma de licitação em cada trimestre de 2021.```")
        st.write("### ```Clique na legenda abaixo para remover do gráfico```")
        st.write("#")

        # Adicionando um dropdown para escolher o trimestre:
        #Criei uma lista para adicionar a opção de escolher o ano no selectbox, e não apenas os valores do semestre
        period = ['Ano Total', 'Trimestre 1', 'Trimestre 2', 'Trimestre 3', 'Trimestre 4']
        selected_period = st.selectbox('Escolha um período:', period)

        #condição para decisão de qual dos dataframes utilizarei
        if selected_period == 'Ano Total':
            df2_filtered = df2_ano
            grafico2(df2_filtered)
        else:
            df2_filtered = df2_trimestre[df2_trimestre['Trimestre'] == selected_period]
            grafico2(df2_filtered)

        st.title("📊 Gráfico 3")
        # st.table(df4)
