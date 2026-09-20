# ===== BASE DE CONHECIMENTO E LOCAIS (R3) =====

ESTACOES = {
    # Linha 1-Azul
    "Pinacoteca": "Luz",
    "Catedral da Sé": "Sé",
    "Centro Cultural São Paulo": "Vergueiro",

    # Linha 2-Verde
    "MASP": "Trianon-Masp",
    "Hospital das Clínicas": "Clínicas",
    "Aquário de São Paulo": "Santos-Imigrantes",

    # Linha 3-Vermelha
    "Theatro Municipal": "Anhangabaú",
    "Memorial da América Latina": "Palmeiras-Barra Funda",
    "Neo Química Arena": "Corinthians-Itaquera"
}

def consultar(fatos, predicado):
    return [f[1:] for f in fatos if f[0] == predicado]

def fatos_base(linhas, locais):
    fatos = set()
    for nome_linha, estacoes in linhas.items():
        for estacao in estacoes:
            fatos.add(("estacao", estacao))
            fatos.add(("pertence", estacao, nome_linha))
            
    for local, estacao in locais.items():
        fatos.add(("proximo_de", local, estacao))
    return fatos



def r_integracao(fatos):

    novos = set()
    pertences = consultar(fatos, "pertence")
    
    for e1, l1 in pertences:
        for e2, l2 in pertences:
            if e1 == e2 and l1 != l2:
                novos.add(("integracao", e1))
    return novos

def r_linha_paralisada(fatos):

    novos = set()
    paralisadas = consultar(fatos, "linha_paralisada")
    pertences = consultar(fatos, "pertence")
    
    for (linha_paralisada,) in paralisadas:
        for estacao, linha_da_estacao in pertences:
            if linha_paralisada == linha_da_estacao:
                novos.add(("bloqueada", estacao))
    return novos
