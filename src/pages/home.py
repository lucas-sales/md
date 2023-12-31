import streamlit as st
from PIL import Image
import os

def write():

    image_logo = Image.open(os.path.abspath("images/logo_ufrpe.jpg"))
    image_bsi = Image.open(os.path.abspath("images/bsi.jpg"))

    col1, col2 = st.columns(2)

    with st.container():
        with col1:
            st.image(image_logo, caption='UFRPE', width=200)
        with col2:
            st.image(image_bsi, caption='BSI', width=200)

    st.write(
        """
        # Despesas Orçamentárias - Home
        """
    )
    st.divider()

    st.write(
        """
            Escolhemos fazer utilização da base de dados de despesas orçamentárias da prefeitura de Recife, 
        pois ela fornece acesso a dados detalhados, permitindo análises históricas e embasamento para tomada de decisões. 
        O cruzamento dessas informações com outras fontes enriquece a análise. Além do mais, promove transparência e prestação de 
        contas, fortalecendo a relação entre governo e sociedade. Com isso, é possível otimizar recursos, planejar estrategicamente e 
        melhorar a qualidade de vida dos cidadãos.""")
    
    st.write("""
        ## Perguntas - DB Tradicional
             1 - Quanto é a média líquida paga pelos 50 maiores credores no primeiro semestre de 2021?

            2 - Qual o valor empenhado total para cada ação em cada trimestre do ano de 2021?

            3 - Qual a quantidade de pagamentos, a média mensal e o valor total por mês no ano de 2021?

            4 - Qual a quantidade de credores por ação e sua média de valor líquido por ação a cada quadrimestre do ano de 2021?

            5 - Qual o total e a média de valor liquidado em licitações classificadas com nome “INEXIGIBILIDADE” e sua respectiva fonte de janeiro a julho dos últimos 2 anos?
""")

    st.divider()

    st.write("""
            ## Perguntas - DW
                1 - Quais os 20 maiores valores pagos e liquidados, bem como a diferença entre os valores para cada credor ao longo do tempo?

                2 - Qual a porcentagem de gastos totais gerados por cada modalidade de licitação?

                3 - Quais são os 10 principais credores com base no valor total pago?

                4 - Tendência Trimestral de Pagamento: Através de um gráfico de linha é possível mostrar as tendências trimestrais nos valores pagos, liquidados e empenhados?

                5 - Durante o período chuvoso(Abril, maio, junho, julho e agosto), há gastos em urbanização na cidade do Recife?

    """)
    
    

        