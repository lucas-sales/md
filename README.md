# Projeto de Modelagem de dados

## UFRPE-BSI 2022.2

Este repositorio tem por objetivo exibir os resultados da pesquisa do grupo 4. A disciplina é Modelagem de dados,
ministrada pela professora Maria da conceição.

## Dependências

O projeto foi escrito em python, as bibliotecas utilizadas estão listadas e versionadas no arquivo "requirements.txt".
Para instalar as dependências no arquivo, executte o comando abaixo:

    pip install -r requirements.txt

## Variaveis de ambiente

Para que seja possível executar este projeto, é necessario configurar um arquivo '.env' na pasta raiz.
Este arquivo deve conter as seguintes informações:

    MYSQL_USER=xxxx
    MYSQL_PASSWORD=xxxx
    MYSQL_HOST=localhost
    MYSQL_PORT=3306
    MYSQL_DB=xxxx
    MYSQL_DB_DW=xxxxx

Obs: A estrutura deve ser igual a descrita acima.

## Executando o projeto

Para executar o projeto basta rodar o seguinte comando no terminal, dentro da pasta:

    streamlit run .\main.py

A seguir, acesse a url *http://localhost.com:8501*
