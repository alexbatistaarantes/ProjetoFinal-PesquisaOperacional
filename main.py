from csv import DictReader

from solucao import solucionar
from carregarDados import carregarDados, carregarCsv

CUSTO_DESLOCAMENTO_POR_UNIDADE = 0.7
CUSTO_TOTAL = 200
MERCADOS, PRODUTOS, PRECOS, HOTEIS, DISTANCIAS = carregarDados()   

def resolver(listaDeCompras, codHotel):
    produtosComprados, mercadosIdos, gasto = solucionar(MERCADOS.keys(), listaDeCompras, PRECOS, DISTANCIAS[codHotel], CUSTO_DESLOCAMENTO_POR_UNIDADE, CUSTO_TOTAL)
    
    print(f"\nPara o hotel {HOTEIS[codHotel]}")

    # Mostrando lista de compras
    print("\n\033[1m LISTA DE COMPRAS: \n")
    for cod in listaDeCompras.keys():
        nome = PRODUTOS[cod]['nome']
        quantidade = listaDeCompras[cod]
        print('{}: {}'.format(nome.ljust(22), quantidade), end="\t")
        if cod%3 == 0:
            print('\n')
    print('\033[0m ')

    print(f"\nCusto total = R$ {gasto} \n")

    for codMercado in MERCADOS.keys():

        if mercadosIdos[codMercado].value() == 1:
            nomeMercado = MERCADOS[codMercado]
            distancia = DISTANCIAS[codHotel][codMercado]
            custoDeslocamento = distancia*2*CUSTO_DESLOCAMENTO_POR_UNIDADE

            print(f"Mercado - {nomeMercado}:")
            print(f" - Custo deslocamento ({distancia}km) = R$ {custoDeslocamento}")
            for codProduto in listaDeCompras.keys():

                if produtosComprados[codMercado, codProduto].value() == 1:
                    nomeProduto = PRODUTOS[codProduto]['nome']
                    quantidade = listaDeCompras[codProduto]
                    precoUnitario = PRECOS[codMercado, codProduto]
                    precoTotal = quantidade*precoUnitario
                    print(f" - {quantidade}un de {nomeProduto} (R$ {precoUnitario}) = R$ {precoTotal}")

def listarProdutos():
    print(" PRODUTOS")
    for cod in PRODUTOS.keys():
        print('{}: {}'.format(cod, f"{PRODUTOS[cod]['nome']}".ljust(22)), end="\t")
        if cod%3 == 0:
            print('\n')
    print('\n')

def carregarListaDeCompras():
    # Dando instrução para criar lista de compras
    input("\033[1m Edite o arquivo \033[4m listaDeCompras.csv \033[0m usando os códigos de produtos e quantidade desejada (aperte Enter para continuar)\033[0m")
    print('\n')

    # Carregando lista de compras
    linhas = carregarCsv("listaDeCompras.csv")
    listaDeCompras = {int(linha['CodProduto']): int(linha['Quantidade']) for linha in linhas}   

    return listaDeCompras

def main():
    
    listarProdutos()

    listaDeCompras = carregarListaDeCompras()

    # Listando Hoteis
    print(" HOTEIS")
    print('\n'.join([f"{cod}: {HOTEIS[cod]}" for cod in HOTEIS.keys()]))
    try:
        # Solicitando código do hotel
        codHotel = int(input("\n\033[1m Digite o código do hotel (ou aperte Enter para realizar a otimização da lista para todos os hoteis):\033[0m "))

        # Resolvendo para um hotel
        resolver(listaDeCompras, codHotel)

    except:
        # Resolvendo para todos os hoteis
        for cod in HOTEIS.keys():
            resolver(listaDeCompras, cod)

main()

