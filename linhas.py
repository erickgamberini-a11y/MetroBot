# ===== DESAFIO: MetrôBot SP 2.0 =====
from collections import deque

# Estruturas de dados fornecidas no PDF
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

def construir_grafo_multilinhas(linhas):

    grafo = {}
    linhas_do_trecho = {}

    for nome_linha, estacoes in linhas.items():
        for i in range(len(estacoes) - 1):
            a = estacoes[i]
            b = estacoes[i + 1]

            if a not in grafo:
                grafo[a] = []
            if b not in grafo:
                grafo[b] = []

            if b not in grafo[a]:
                grafo[a].append(b)
            if a not in grafo[b]:
                grafo[b].append(a)

            if (a, b) not in linhas_do_trecho:
                linhas_do_trecho[(a, b)] = set()
            if (b, a) not in linhas_do_trecho:
                linhas_do_trecho[(b, a)] = set()
            
            linhas_do_trecho[(a, b)].add(nome_linha)
            linhas_do_trecho[(b, a)].add(nome_linha)

    return grafo, linhas_do_trecho

def contar_baldeacoes(caminho, linhas_do_trecho):

    if not caminho or len(caminho) < 2:
        return 0, []

    quantidade = 0
    lista_baldeacoes = []

    estacao_atual = caminho[0]
    proxima_estacao = caminho[1]
    linha_atual = list(linhas_do_trecho[(estacao_atual, proxima_estacao)])[0]

    for i in range(1, len(caminho) - 1):
        estacao_a = caminho[i]
        estacao_b = caminho[i + 1]
        linhas_proximo_trecho = linhas_do_trecho[(estacao_a, estacao_b)]

        if linha_atual not in linhas_proximo_trecho:
            quantidade += 1
            nova_linha = list(linhas_proximo_trecho)[0]
            lista_baldeacoes.append((estacao_a, nova_linha))
            linha_atual = nova_linha

    return quantidade, lista_baldeacoes

GRAFO, LINHAS_DO_TRECHO = construir_grafo_multilinhas(LINHAS)