# -- 1 - Calcular os 20 maiores valores pagos e liquidados, bem como a diferença entre os valores para cada credor ao longo do tempo
QUERY1 = """SELECT
    c.nome AS 'credor',
    t.ano_id AS 'ano',
    t.mes_texto AS 'mes',
    t.trimestre_numeronoano AS 'trimestre',
    SUM(p.valor_pago) AS 'Valor Pago Total',
    SUM(p.valor_liquidado) AS 'Valor Liquidado Total',
    SUM(p.valor_pago - p.valor_liquidado) AS 'Diferença Pago Liquidado'
FROM
    ft_pagamento p
JOIN
    dm_credor c ON p.cod_credor = c.key
JOIN
    dm_data t ON p.cod_tempo = t.keyData
GROUP BY
    c.nome, t.ano_id, t.mes_texto, t.trimestre_numeronoano
ORDER BY
   SUM(p.valor_pago - p.valor_liquidado) DESC;
"""

# -- 2 - Qual a porcentagem de gastos totais gerados por cada modalidade de licitação?;
QUERY2 = """SELECT
    ml.nome AS 'Modalidade Nome',
    trimestre_texto AS 'Trimestre',
    SUM(p.valor_pago) AS 'Valor Total'
FROM
    ft_pagamento p
JOIN
    dm_modalidade_licitacao ml ON p.cod_modalidade_licitacao = ml.key
JOIN
	dm_data d ON p.cod_tempo = d.keyData
GROUP BY
    ml.nome, trimestre_texto;
"""
QUERY2_1 ="""SELECT
    ml.nome AS 'Modalidade Nome',
    SUM(p.valor_pago) AS 'Valor Total'
FROM
    ft_pagamento p
JOIN
    dm_modalidade_licitacao ml ON p.cod_modalidade_licitacao = ml.key
GROUP BY
    ml.nome;"""

# -- 3 - Quais são os 10 principais credores com base no valor total pago?

QUERY3 ="""SELECT c.nome AS credor, SUM(p.valor_pago) AS valor_total_pago
FROM dm_credor c
JOIN ft_pagamento p ON c.`key` = p.cod_credor
GROUP BY c.nome
ORDER BY valor_total_pago DESC
LIMIT 10;"""

# 4 - Tendência Trimestral de Pagamento: Através de um gráfico de linha é possível
#     mostrar as tendências trimestrais nos valores pagos, liquidados e empenhados?
QUERY4 ="""SELECT
    d.trimestre_texto,
    SUM(p.valor_pago) AS valor_pago_trimestre,
    SUM(p.valor_liquidado) AS valor_liquidado_trimestre,
    SUM(p.valor_empenhado) AS valor_empenhado_trimestre
FROM
    ft_pagamento p
JOIN
    dm_data d ON p.cod_tempo = d.keyData
GROUP BY
	d.trimestre_texto
ORDER BY
    d.trimestre_texto;"""

# 5 - Durante o período chuvoso(Abril, maio, junho, julho e agosto),
#     há gastos em urbanização na cidade do Recife?
QUERY5 = """SELECT
    mes_texto,
    a.nome AS acao,
    SUM(p.valor_pago) AS valor_total_pago
FROM
    ft_pagamento p
JOIN
    dm_data d ON p.cod_tempo = d.keyData
JOIN
    dm_acao a ON p.cod_acao = a.key
WHERE
    d.mes_texto IN ('Abr', 'Mai', 'Jun', 'Jul', 'Ago')
GROUP BY
    d.mes_texto, a.nome
ORDER BY
	d.mes_texto, valor_total_pago DESC
LIMIT 10;"""