import pulp

def solucionar(mercados, produtos, precos, distancias, custoDeslocamento, custoMaximo):

    # Definir o modelo
    model = pulp.LpProblem('Compras', sense=pulp.LpMinimize)

    # Adicionar as variáveis, com valor mínimo de 0
    x = pulp.LpVariable.dicts(indexs=precos.keys(), cat=pulp.LpBinary, lowBound=0, name='produtos-mercado')
    y = pulp.LpVariable.dicts(indexs=mercados, cat=pulp.LpBinary, lowBound=0, name='mercados')

    # Restrição 1
    # Define que um de cada produto deve ser comprado
    for codProduto in produtos.keys():
        model.addConstraint( 
            sum( [x[codMercado,codProduto] for codMercado in mercados] ) == 1,
            name=f'restrição_1_{codProduto}'
        )

    # Restrição 2
    # Define que se pelo menos um produto deve ser comprado em um mercado, a variavel de deslocamento para este mercado deve ser 1
    for codMercado in mercados:
        [ model.addConstraint( x[codMercado,codProduto] <= y[codMercado], name=f'restrição_2_{codMercado}_{codProduto}') for codProduto in produtos.keys() ]

    # Restrição 3
    # Limite de custo total
    model.addConstraint(
        sum(produtos[codProduto]*precos[codMercado,codProduto]*x[codMercado,codProduto] for codMercado in mercados for codProduto in produtos)
        +
        sum((custoDeslocamento * 2 * distancias[codMercado]) * y[codMercado] for codMercado in mercados)
        <= custoMaximo,
        name='restrição_custo_total'
    )

    model.setObjective(
        sum(produtos[codProduto]*precos[codMercado,codProduto]*x[codMercado,codProduto] for codMercado in mercados for codProduto in produtos)
        +
        sum((custoDeslocamento * 2 * distancias[codMercado]) * y[codMercado] for codMercado in mercados)
    )

    # Soluciona
    # Define solver explicitamente para poder não mostrar log da resolução
    model.solve( pulp.PULP_CBC_CMD(msg=False) )

    return x, y, pulp.value(model.objective)

