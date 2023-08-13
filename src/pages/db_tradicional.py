import numpy as np
import streamlit as st
import pandas as pd

from src.config import config
from src.database import queries
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
        database=config.MYSQL_DATABASE
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

    # Buscando e configurando os dados para cada consulta

    # Carregando dados da QUERY 1
    df1 = fetch_data(db, queries.QUERY1, ['nome_credor', 'media_liquida_semestral'])
    # Carregando dados da QUERY 2
    df2 = fetch_data(db, queries.QUERY2, ['trimestre', 'codigo_acao', 'nome_acao', 'valor_empenhado_total', 'ano'])
    # Carregando dados da QUERY 3
    df3 = fetch_data(db, queries.QUERY3, ['mes_movimentacao', 'quantidade_pagamentos', 'total_pagamentos'])
    # Carregando dados da QUERY 4
    df4 = fetch_data(db, queries.QUERY4,
                     ['quadrimestre', 'nome_acao', 'quantidade_creditos', 'media_valor_liquido_acao'])
    # Carregando dados da QUERY 5
    df5 = fetch_data(db, queries.QUERY5,
                     ['ano_movimentacao', 'nome_fonte', 'total_valor_liquidado', 'media_valor_liquidado'])

    # Exibe os dados no Streamlit
    with st.spinner("Loading..."):

        st.title(' 🖥 Banco Tradicional')
        st.subheader('Gráficos que demonstram o resultado de algumas perguntas feitas a base '
                     '"_Despesas Orçamentárias de Recife_"')
        st.divider()

        st.title("📊 Gráfico 1")
        st.write("> # 1 - Quanto é a média líquida paga pelos 50 maiores credores no primeiro semestre de 2021?")
        st.write("#### ```Utilize o slide para selecionar a quantidade de credores que deseja visualizar, "
                 "e tenha acesso a média líquida paga por eles no 1º Semestre de 2021.```")
        st.write("#")
        # Adicionei aqui um filtro para selecionar a quantidade de maiores credores
        num_credores = st.slider("Selecione a quantidade de maiores credores:", 5, 50, 50, 5)

        # Filtrando aqui o dataframe com base na seleção
        df1_filtered = df1.head(num_credores)

        # Renomeei a coluna pra ficar com um nome mais legal
        df1_filtered = df1_filtered.rename(columns={'media_liquida_semestral': 'Média Líquida Semestral'})

        # Plotando o gráfico, utilizando o gráfico de barras, só que na horizontal
        st.bar_chart(df1_filtered.set_index('nome_credor').sort_values(by='Média Líquida Semestral', ascending=True))

        st.divider()

        st.title("📊 Gráfico 2")
        st.write("> # 2 - Qual o valor empenhado total para cada ação em cada trimestre do ano de 2021?")
        st.write("#### ```Utilize o dropdown para selecionar a ação, e ter acesso a todos"
                 "aos valores empenhados por ela em cada trimestre de 2021.```")
        st.write("#")

        # Lista de todos os trimestres possíveis:
        all_trimesters = ['1º Trimestre', '2º Trimestre', '3º Trimestre', '4º Trimestre']

        # Garantindo uma linha para cada combinação de nome_acao e trimestre
        df2_complete = pd.DataFrame({
            'trimestre': all_trimesters * len(df2['nome_acao'].unique()),
            'nome_acao': np.repeat(df2['nome_acao'].unique(), len(all_trimesters))
        })

        # Juntando (merge) com os dados originais para preencher os valores
        df2_merged = pd.merge(df2_complete, df2, on=['trimestre', 'nome_acao'], how='left').fillna(0)

        # Adicionando um dropdown para selecionar a ação:
        acao_selected = st.selectbox('Escolha uma ação:', df2['nome_acao'].unique())

        # Filtrando o DataFrame com base na seleção:
        df2_filtered = df2_merged[df2_merged['nome_acao'] == acao_selected]

        # Plotando o gráfico de barras para a ação selecionada ao longo de todos os trimestres:
        st.bar_chart(df2_filtered.set_index('trimestre')['valor_empenhado_total'])

        st.divider()

        st.title("📊 Gráfico 3")
        st.write("> # 3 - Qual a quantidade de pagamentos, a média mensal e o valor total por mês no ano de 2021?")
        st.write("#### ```Utilize o dropdown para selecionar qual tipo de visualização você deseja: "
                 "Quantidades de pagamentos, total de pagamentos ou média mensal de pagamentos. ```")

        st.write("#")

        # Dicionário de conversão
        month_mapping = {
            1.0: 'JAN',
            2.0: 'FEV',
            3.0: 'MAR',
            4.0: 'ABR',
            5.0: 'MAI',
            6.0: 'JUN',
            7.0: 'JUL',
            8.0: 'AGO',
            9.0: 'SET',
            10.0: 'OUT',
            11.0: 'NOV',
            12.0: 'DEZ'
        }

        # Convertendo a coluna mes_movimentacao
        df3['mes_movimentacao'] = df3['mes_movimentacao'].map(month_mapping)

        # Calculando a média mensal de pagamentos
        df3['media_mensal_pagamentos'] = df3['total_pagamentos'] / df3['quantidade_pagamentos']

        # Mapeando as métricas com descrições amigáveis
        metrics_options = {
            "Quantidade de Pagamentos": "quantidade_pagamentos",
            "Total de Pagamentos": "total_pagamentos",
            "Média Mensal de Pagamentos": "media_mensal_pagamentos"
        }

        friendly_names = {
            "quantidade_pagamentos": "Quantidade de Pagamentos",
            "total_pagamentos": "Total de Pagamentos",
            "media_mensal_pagamentos": "Média Mensal de Pagamentos"
        }

        # Dropdown para escolher a métrica
        chosen_metric = st.selectbox('Escolha uma métrica para visualizar:', list(metrics_options.keys()))

        # Plotando o gráfico de acordo com a métrica escolhida
        data_to_plot = df3.set_index('mes_movimentacao')[[metrics_options[chosen_metric]]]
        data_to_plot.columns = [friendly_names[metrics_options[chosen_metric]]]

        if chosen_metric == "Quantidade de Pagamentos":
            st.bar_chart(data_to_plot)
        else:
            st.line_chart(data_to_plot)

        st.divider()

        # Aqui na query  4 fiz tipo a query 2, plotando apenas as colunas quadrimestre (como índice)
        # e media_valor_liquido_acao, mas dá pra modificar
        st.title("📊 Gráfico 4")
        st.write("> # 4 - Qual a quantidade de credores por ação e sua média de valor líquido por ação "
                 "a cada quadrimestre do ano de 2021?")
        st.write("#### ```Utilize o dropdown pra selecionar a ação e em seguida escolha a métrica que "
                 "deseja visualizar.```")

        st.write("#")

        # Criando um dropdown para escolher a ação
        acao_selected = st.selectbox("Selecione a ação:", df4["nome_acao"].unique())

        # Filtrando o dataframe pela ação escolhida
        df4_filtered = df4[df4["nome_acao"] == acao_selected]

        # Opções de métrica e nomes amigáveis
        metrics_options = {
            "Quantidade de Créditos": "quantidade_creditos",
            "Média de Valor Líquido": "media_valor_liquido_acao"
        }
        friendly_names = {
            "quantidade_creditos": "Quantidade de Créditos",
            "media_valor_liquido_acao": "Média de Valor Líquido"
        }
        st.write("#")
        # Escolhendo a métrica para visualizar
        chosen_metric = st.radio("Escolha a métrica para visualizar:", list(metrics_options.keys()))
        st.write("#")
        # Plotando o gráfico
        st.bar_chart(df4_filtered.set_index('quadrimestre')[metrics_options[chosen_metric]].rename(
            friendly_names[metrics_options[chosen_metric]]))

        st.divider()

        st.title("📊 Gráfico 5")
        st.write("> # 5 - Qual o total e a média de valor liquidado em licitações classificadas "
                 "com nome “INEXIGIBILIDADE” e sua respectiva fonte de janeiro a julho dos últimos 2 anos?")
        st.write("#### ```Utilize o dropdown pra selecionar a fonte e visualizar o total e a média"
                 " da fonte selecionada.```")

        st.write("#")

        # Adiciona um filtro para o nome_fonte
        fonte_options = list(df5['nome_fonte'].unique())
        selected_fonte = st.selectbox("Selecione a fonte:", fonte_options)

        # Filtra o dataframe com base na seleção
        df5_filtered = df5[df5['nome_fonte'] == selected_fonte]

        df5_pivot = df5_filtered.pivot_table(index='ano_movimentacao', columns='nome_fonte',
                                             values='total_valor_liquidado', aggfunc='mean').reset_index()
        st.bar_chart(df5_pivot.set_index('ano_movimentacao'))



