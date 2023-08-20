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

# -- 1 - mostrar a distribuição percentual dos gastos por modalidade de licitação.
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
QUERY3 ="""SELECT
    ml.nome AS 'Modalidade Nome',
    SUM(p.valor_pago) AS 'Valor Total'
FROM
    ft_pagamento p
JOIN
    dm_modalidade_licitacao ml ON p.cod_modalidade_licitacao = ml.key
GROUP BY
    ml.nome;"""

