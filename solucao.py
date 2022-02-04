import pulp

def calcularSolucao(listaDeCompras, mercados, distancias, custoDeslocamentoPorUnidade):
     
    # Definir o modelo
    model = pulp.LpProblem('Compras', sense=pulp.LpMinimize)

    # Adicionar as variáveis, com valor mínimo de 0
    x = pulp.LpVariable.dicts(indexs=[i for i in mercados.keys()], cat=pulp.LpContinuous, lowBound=0, name='x')

    # Gerando restrições
    restricao_1 = " + ".join( [f"x[{cod}]" for cod in mercados.keys()] )
    restricao_1 += " == 1"
    model.addConstraint(eval(restricao_1), name='restricao_1')

    # Gerando função objetivo
    funcaoObjetivo = ""
    for codMercado in mercados.keys():

        mercado = mercados[codMercado]
        produtos = mercado['produtos']

        custoCompras = sum([(listaDeCompras[codProd] * produtos.get(codProd)) for codProd in listaDeCompras.keys()])
        custoDeslocamento = distancias[codMercado] * custoDeslocamentoPorUnidade
        custoTotal = custoCompras + custoDeslocamento

        funcaoObjetivo += f"{custoTotal} * x[{codMercado}] + "

    # Retirando trailing +
    funcaoObjetivo = funcaoObjetivo.rstrip('+ ')

    # Função Objetivo gerada dinamicamente
    model.setObjective( eval(funcaoObjetivo) )

    # Optimizar
    # Define solver explicitamente para poder não mostrar log da resolução
    model.solve( pulp.PULP_CBC_CMD(msg=False) )

    # Retorna a solução
    codMercado = [cod for cod in x.keys() if x[cod].value() == 1][0]
    custoDaCompra = pulp.value(model.objective)
    return codMercado, custoDaCompra

