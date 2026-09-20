# dados.py
LINHAS = {
    "Linha 1-Azul": [
        "Tucuruvi", "Parada Inglesa", "Jardim São Paulo", "Santana",
        "Carandiru", "Portuguesa-Tietê", "Armênia", "Tiradentes", "Luz",
        "São Bento", "Sé", "Japão-Liberdade", "São Joaquim", "Vergueiro",
        "Paraíso", "Ana Rosa", "Vila Mariana", "Santa Cruz",
        "Praça da Árvore", "Saúde", "São Judas", "Conceição", "Jabaquara"
    ],
    "Linha 2-Verde": [
        "Vila Madalena", "Sumaré", "Clínicas", "Consolação", "Trianon-Masp",
        "Brigadeiro", "Paraíso", "Ana Rosa", "Chácara Klabin",
        "Santos-Imigrantes", "Alto do Ipiranga", "Sacomã", "Tamanduateí",
        "Vila Prudente"
    ],
    "Linha 3-Vermelha": [
        "Palmeiras-Barra Funda", "Marechal Deodoro", "Santa Cecília",
        "República", "Anhangabaú", "Sé", "Pedro II", "Brás",
        "Bresser-Mooca", "Belém", "Tatuapé", "Carrão", "Penha",
        "Vila Matilde", "Guilhermina-Esperança", "Patriarca-Vila Ré",
        "Artur Alvim", "Corinthians-Itaquera"
    ]
}

CORES = {
    "Linha 1-Azul": "#1e88e5",
    "Linha 2-Verde": "#2e7d32",
    "Linha 3-Vermelha": "#d32f2f"
}

LOCAIS = {
    "Pinacoteca": "Luz",
    "Catedral da Sé": "Sé",
    "Centro Cultural São Paulo": "Vergueiro",
    "MASP": "Trianon-Masp",
    "Hospital das Clínicas": "Clínicas",
    "Aquário de São Paulo": "Santos-Imigrantes",
    "Theatro Municipal": "Anhangabaú",
    "Memorial da América Latina": "Palmeiras-Barra Funda",
    "Neo Química Arena": "Corinthians-Itaquera"
}

# Criar lista plana com todas as estações para o LLM
TODAS_ESTACOES = []
for estacoes in LINHAS.values():
    TODAS_ESTACOES.extend(estacoes)
TODAS_ESTACOES = list(set(TODAS_ESTACOES)) # Remover duplicados como Sé e Paraíso

def construir_grafo_multilinhas(linhas):
    grafo = {}
    linhas_do_trecho = {}
    for nome_linha, estacoes in linhas.items():
        for i in range(len(estacoes) - 1):
            a, b = estacoes[i], estacoes[i + 1]
            if a not in grafo: grafo[a] = []
            if b not in grafo: grafo[b] = []
            if b not in grafo[a]: grafo[a].append(b)
            if a not in grafo[b]: grafo[b].append(a)
            
            if (a, b) not in linhas_do_trecho: linhas_do_trecho[(a, b)] = set()
            if (b, a) not in linhas_do_trecho: linhas_do_trecho[(b, a)] = set()
            linhas_do_trecho[(a, b)].add(nome_linha)
            linhas_do_trecho[(b, a)].add(nome_linha)
    return grafo, linhas_do_trecho

GRAFO, LINHAS_DO_TRECHO = construir_grafo_multilinhas(LINHAS)

def contar_baldeacoes(caminho, linhas_do_trecho):
    if not caminho or len(caminho) < 2: return 0, []
    quantidade = 0
    lista_baldeacoes = []
    linha_atual = list(linhas_do_trecho[(caminho[0], caminho[1])])[0]
    
    for i in range(1, len(caminho) - 1):
        a, b = caminho[i], caminho[i + 1]
        linhas_prox = linhas_do_trecho[(a, b)]
        if linha_atual not in linhas_prox:
            quantidade += 1
            nova_linha = list(linhas_prox)[0]
            lista_baldeacoes.append((a, nova_linha))
            linha_atual = nova_linha
    return quantidade, lista_baldeacoes