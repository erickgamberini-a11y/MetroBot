# busca.py
from collections import deque

def reconstruir_caminho(pai, destino):
    caminho = []
    atual = destino
    while atual is not None:
        caminho.append(atual)
        atual = pai[atual]
    return list(reversed(caminho))

def bfs(grafo, origem, destino, bloqueadas=()):
    if origem in bloqueadas or destino in bloqueadas:
        return None, []
    fila = deque([origem])
    pai = {origem: None}
    ordem_visita = []
    while fila:
        atual = fila.popleft()
        ordem_visita.append(atual)
        if atual == destino:
            return reconstruir_caminho(pai, destino), ordem_visita
        for vizinho in grafo[atual]:
            if vizinho not in pai and vizinho not in bloqueadas:
                pai[vizinho] = atual
                fila.append(vizinho)
    return None, ordem_visita

def dfs(grafo, origem, destino, bloqueadas=()):
    if origem in bloqueadas or destino in bloqueadas:
        return None, []
    visitados = set()
    ordem_visita = []
    def explorar(atual, caminho):
        visitados.add(atual)
        ordem_visita.append(atual)
        if atual == destino:
            return caminho
        for vizinho in grafo[atual]:
            if vizinho not in visitados and vizinho not in bloqueadas:
                resultado = explorar(vizinho, caminho + [vizinho])
                if resultado: return resultado
        return None
    return explorar(origem, [origem]), ordem_visita