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
    df1 = fetch_data(db, dw_queries.QUERY1, ['credor', 'ano', 'mes', 'trimestre', 'Valor Pago Total',
                                              'Valor Liquidado Total', 'Diferença Pago Liquidado'])

    # Carregando dados da QUERY 2
    df2_trimestre = fetch_data(db, dw_queries.QUERY2, ['Modalidade Nome', 'Trimestre', 'Valor Total'])
    df2_ano = fetch_data(db, dw_queries.QUERY2_1, ['Modalidade Nome', 'Valor Total'])


    #Carregando dados da QUERY 3
    df3 = fetch_data(db, dw_queries.QUERY3, ['credor', 'valor_total_pago'])

    # Carregando dados da QUERY 4
    df4 = fetch_data(db, dw_queries.QUERY4, ['trimestre_texto', 'valor_pago_trimestre', 'valor_liquidado_trimestre',
                                             'valor_empenhado_trimestre'])

    # Carregando dados da QUERY 5
    df5 = fetch_data(db, dw_queries.QUERY5, ['mes_texto', 'acao', 'valor_total_pago'])

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
        st.write("#")

        #Função utilizada para a criação do gráfico da segunda questão
        def grafico2(data):
            fig = px.pie(data, names='Modalidade Nome', values='Valor Total',
                title='Distribuição de Gastos por Modalidade de Licitação')
            st.plotly_chart(fig)

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

        st.divider()

        st.title("📊 Gráfico 3")
        st.write("> # 3 - Quais são os 10 principais credores com base no valor total pago?")
        st.write("#### ``` ```")
        st.write("#")

        # Gerando o gráfico para a pergunta 3:
        fig3 = px.bar(df3, x='credor', y='valor_total_pago',
                      labels={
                          'credor': 'Credor',
                          'valor_total_pago': 'Valor Total Pago'
                      },
                      title='10 Principais Credores com base no Valor Total Pago')
        fig3.update_layout(xaxis={'categoryorder': 'total descending'})
        st.plotly_chart(fig3)

        st.divider()

        st.title("📊 Gráfico 4")
        st.write("> # 4 - Tendência Trimestral de Pagamento: Através de um gráfico de linha é possível "
                 "mostrar as tendências trimestrais nos valores pagos, liquidados e empenhados?")
        st.write("#### ``` Selecione as métricas abaixo e visualize no gráfico de linhas: ```")
        st.write("#")

        # Adicionando um multiselect para permitir que os usuários escolham as métricas
        selected_metrics = st.multiselect('Escolha as métricas:',
                                          options=['Valor Pago Trimestre', 'Valor Liquidado Trimestre',
                                                   'Valor Empenhado Trimestre'],
                                          default=['Valor Pago Trimestre', 'Valor Liquidado Trimestre',
                                                   'Valor Empenhado Trimestre'])

        # Mapeando o nome da métrica selecionada para a coluna correspondente
        metrics_mapping = {
            'Valor Pago Trimestre': 'valor_pago_trimestre',
            'Valor Liquidado Trimestre': 'valor_liquidado_trimestre',
            'Valor Empenhado Trimestre': 'valor_empenhado_trimestre'
        }
        selected_columns = [metrics_mapping[metric] for metric in selected_metrics]

        # Criando um gráfico de linha com as métricas selecionadas
        fig4 = px.line(df4, x='trimestre_texto', y=selected_columns,
                       title='Tendência Trimestral de Pagamento',
                       labels={
                           'trimestre_texto': 'Trimestre',
                           'value': 'Valor'
                       })

        # Adicionando legenda customizada
        for metric in selected_metrics:
            fig4.update_traces(
                hovertemplate=f'<b>%{{x}}</b><br>Valor: %{{y:.2f}}<extra></extra>',
                name=metric,
                selector=dict(variable=metrics_mapping[metric]))

        # Exibindo o gráfico
        st.plotly_chart(fig4)

        st.divider()

        st.title("📊 Gráfico 5")
        st.write("> # Durante o período chuvoso(abril, maio, junho, julho e agosto), "
                 "há gastos em urbanização na cidade do Recife?")
        st.write("#### ``` Selecione as métricas abaixo e visualize no gráfico de linhas: ```")

        st.write("#")

        # Adicionando um dropdown para escolher o mês:
        mes_selected_5 = st.selectbox('Escolha um mês:', ['Todos'] + list(df5['mes_texto'].unique()))

        # Filtrando o DataFrame com base na seleção do mês (se não for 'Todos'):
        if mes_selected_5 != 'Todos':
            df5 = df5[df5['mes_texto'] == mes_selected_5]

        # Pivotando o DataFrame para obter os meses como colunas e as ações como índices
        df5_pivot = df5.pivot_table(index='acao', columns='mes_texto', values='valor_total_pago', fill_value=0)

        # Criando um gráfico de barras empilhadas
        fig5 = px.bar(df5_pivot, x=df5_pivot.index, y=df5_pivot.columns,
                      title='Valor Total Pago por Ação e Mês',
                      labels={'value': 'Valor Total Pago', 'variable': 'Mês', 'index': 'Ação'})

        # Atualizando o layout para melhor visualização
        fig5.update_layout(barmode='stack')

        # Exibindo o gráfico
        st.plotly_chart(fig5)