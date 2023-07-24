# -- 1 - Quanto é a média líquida paga pelos 50 maiores credores no primeiro semestre de 2021?
QUERY1 = """SELECT c.nome AS nome_credor, AVG(p.valor_liquidado) AS media_liquida_semestral
FROM pagamento p
JOIN credor c ON p.cod_credor = c.codigo
WHERE p.mes_movimentacao >= 1 AND p.mes_movimentacao <= 6
GROUP BY p.cod_credor, c.nome
ORDER BY media_liquida_semestral DESC
LIMIT 50;
"""

# -- 2 - Qual o valor empenhado total para cada ação em cada trimestre do ano de 2021?
QUERY2 = """
SELECT
    CASE
        WHEN p.mes_movimentacao  <= 3 THEN '1º Trimestre'
        WHEN p.mes_movimentacao <= 6 THEN '2º Trimestre'
        WHEN p.mes_movimentacao <= 9 THEN '3º Trimestre'
        ELSE '4º Trimestre'
    END AS trimestre,
    a.codigo  AS codigo_acao,
    a.nome  AS nome_acao,
    SUM(e.valor_empenhado) AS valor_empenhado_total,
    '2021' as ano
FROM
    pagamento p
JOIN
    empenho e ON p.codigo = e.codigo
JOIN
    acao a ON p.codigo= a.codigo
WHERE
    p.ano_movimentacao  = 2021
GROUP BY
    trimestre,
    a.codigo ,
    a.nome
ORDER by trimestre, a.codigo;
"""

# -- 3 Qual a quantidade de pagamentos, a média mensal e o valor total por mês no ano de 2021?
QUERY3 = """
SELECT
    mes_movimentacao ,
    COUNT(*) AS quantidade_pagamentos,
    SUM(valor_pago) AS total_pagamentos
FROM
    pagamento
WHERE
    ano_movimentacao  = 2021
GROUP BY    mes_movimentacao 
order by total_pagamentos desc;
"""

# -- 4 - Qual a quantidade de credores por ação e sua média de valor líquido por ação a cada quadrimestre do ano de 2021?
QUERY4 = """
SELECT
    CASE
        WHEN p.mes_movimentacao  <= 4 THEN '1º Quadrimestre'
        WHEN p.mes_movimentacao <= 8 THEN '2º Quadrimestre'
        ELSE '3º Quadrimestre'
    END AS quadrimestre,
    a.nome  AS nome_acao,
    COUNT(DISTINCT p.cod_credor) AS quantidade_creditos,
    AVG(p.valor_liquidado) AS media_valor_liquido
FROM
    pagamento p
JOIN
    acao a ON p.cod_acao  = a.codigo
WHERE
    p.ano_movimentacao  = 2021
GROUP BY
    quadrimestre,
    p.cod_acao,
    a.nome
ORDER BY
    quadrimestre,
    p.cod_acao;
"""

# -- 5 - Qual o total e a média de valor liquidado em licitações classificadas com nome “INEXIGIBILIDADE” e sua respectiva fonte de janeiro a julho dos últimos 2 anos?
QUERY5 = """
SELECT
    p.ano_movimentacao ,
    f.nome AS nome_fonte,
    SUM(p.valor_liquidado) AS total_valor_liquidado,
    AVG(p.valor_liquidado) AS media_valor_liquidado
FROM
    pagamento p
JOIN
    modalidade_licitacao m ON p.cod_modalidade_licitacao  = m.codigo
JOIN
    fonte f ON p.cod_fonte  = f.codigo
WHERE
    m.nome = 'INEXIGIBILIDADE'
    AND p.mes_movimentacao  >= 1 AND p.mes_movimentacao  <= 7
    AND p.ano_movimentacao  >= YEAR(CURDATE()) - 2 AND p.ano_movimentacao  <= YEAR(CURDATE()) - 1
GROUP BY
    p.ano_movimentacao ,
    p.cod_fonte ,
    f.nome;
"""