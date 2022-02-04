from csv import DictReader

CAMINHO_PRECOS = 'dados/dados.csv'
CAMINHO_HOTEIS = 'dados/hoteis.csv'
CAMINHO_MERCADOS = 'dados/mercados.csv'
CAMINHO_DISTANCIAS = 'dados/distancias.csv'

def carregarCsv(caminhoCsv):
    """ Retorna uma tabela a partir do arquivo .csv, no formato de lista de dicionários
    """

    with open(caminhoCsv, 'r', newline='') as csvFile:
        reader = DictReader(csvFile, delimiter=',')
        linhas = list(reader)

    return linhas

def carregarDados():
    """ Carrega e retorna todos os dados da aplicação
    """

    # Mercados
    linhas = carregarCsv( CAMINHO_MERCADOS )
    mercados = {int(linha['Código']): {'nome': linha['Supermercado'], 'produtos': {}} for linha in linhas}

    # Preços
    linhas = carregarCsv( CAMINHO_PRECOS )
    produtos = {}
    for linha in linhas:
        codProduto = int(linha['Cod'])
        nomeProduto = linha['Produto']
        categoriaProduto = linha['Seção']
        produtos[codProduto] = {'nome': nomeProduto, 'categoria': categoriaProduto}

        for codMercado in mercados.keys():
            mercado = mercados[codMercado]
            precoProduto = float(linha[str(codMercado)].replace(',', '.'))
            mercado['produtos'][codProduto] = precoProduto
    
    # Hotéis
    linhas = carregarCsv( CAMINHO_HOTEIS )
    hoteis = {int(linha['Código']): linha['Hotel'] for linha in linhas}
    
    # Distâncias
    linhas = carregarCsv( CAMINHO_DISTANCIAS )
    distancias = {}
    for linha in linhas:
        codHotel = int(linha['Hotel'])
        distancias[codHotel] = {codMercado: float(linha[str(codMercado)]) for codMercado in mercados.keys()}

    return mercados, produtos, hoteis, distancias

