# -- 1 - Calcular os 20 maiores valores pagos e liquidados, bem como a diferença entre os valores para cada credor ao longo do tempo
QUERY1 = """SELECT
    c.nome AS credor,
    t.ano_id AS ano,
    t.mes_texto AS mes,
    t.trimestre_numeronoano AS trimestre,
    SUM(p.valor_pago) AS valor_pago_total,
    SUM(p.valor_liquidado) AS valor_liquidado_total,
    SUM(p.valor_pago - p.valor_liquidado) AS diferenca_pago_liquidado
FROM
    ft_pagamento p
JOIN
    dm_credor c ON p.cod_credor = c.key
JOIN
    dm_data t ON p.cod_tempo = t.keyData
GROUP BY
    c.nome, t.ano_id, t.mes_texto, t.trimestre_numeronoano
ORDER BY
   diferenca_pago_liquidado DESC;
"""