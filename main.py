from csv import DictReader

from solucao import calcularSolucao
from carregarDados import carregarDados, carregarCsv

MERCADOS, PRODUTOS, HOTEIS, DISTANCIAS = carregarDados()   
DINHEIRO_DISPONIVEL= 200
CUSTO_DESLOCAMENTO_POR_UNIDADE = 0.7

def resolver(listaDeCompras, codHotel):
    codMercado, custo = calcularSolucao(listaDeCompras, MERCADOS, DISTANCIAS[codHotel], CUSTO_DESLOCAMENTO_POR_UNIDADE)
    nomeMercado = MERCADOS[codMercado]['nome']
    nomeHotel = HOTEIS[codHotel]

    if custo > DINHEIRO_DISPONIVEL:
        print(f"O dinheiro disponível de R$ {DINHEIRO_DISPONIVEL} não é suficiente")
        print(f"{nomeHotel} -> {nomeMercado}: R$ {custo}.")

    else:
        print(f"{nomeHotel} -> {nomeMercado}: R$ {custo}.")

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

    # Mostrando lista de compras
    print("\n\033[1m LISTA DE COMPRAS: \n")
    for cod in listaDeCompras.keys():
        nome = PRODUTOS[cod]['nome']
        quantidade = listaDeCompras[cod]
        print('{}: {}'.format(nome.ljust(22), quantidade), end="\t")
        if cod%3 == 0:
            print('\n')
    print('\033[0m \n')

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
        resolver(listaDeCompras, codHotel)
    except:
        for cod in HOTEIS.keys():
            resolver(listaDeCompras, cod)

main()

