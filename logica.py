# logica.py
from itertools import product
from linhas import LINHAS, LOCAIS

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

def r_origem(fatos):
    novos = set()
    for (local,) in consultar(fatos, "usuario_esta_em"):
        for (l, e) in consultar(fatos, "proximo_de"):
            if l == local: novos.add(("origem", e))
    for (e,) in consultar(fatos, "usuario_esta_na_estacao"):
        novos.add(("origem", e))
    return novos

def r_destino(fatos):
    novos = set()
    for (local,) in consultar(fatos, "usuario_quer_ir"):
        for (l, e) in consultar(fatos, "proximo_de"):
            if l == local: novos.add(("destino", e))
    for (e,) in consultar(fatos, "usuario_quer_ir_estacao"):
        novos.add(("destino", e))
    return novos

def r_bloqueio(fatos):
    return {("bloqueada", e) for (e,) in consultar(fatos, "fechada")}

def r_acessibilidade(fatos):
    if not consultar(fatos, "precisa_acessibilidade"): return set()
    return {("inacessivel", e) for (e,) in consultar(fatos, "elevador_em_manutencao")}

def r_alerta(fatos):
    novos = set()
    inacessiveis = {e for (e,) in consultar(fatos, "inacessivel")}
    for papel in ("origem", "destino"):
        for (e,) in consultar(fatos, papel):
            if e in inacessiveis: novos.add(("alerta", papel, e))
    return novos

def r_integracao(fatos):
    novos = set()
    pertences = consultar(fatos, "pertence")
    for e1, l1 in pertences:
        for e2, l2 in pertences:
            if e1 == e2 and l1 != l2: novos.add(("integracao", e1))
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

REGRAS = [
    ("R1 origem", "Vl Ve (usuario_esta_em(l) ^ proximo_de(l,e) -> origem(e))", r_origem),
    ("R2 destino", "Vl Ve (usuario_quer_ir(l) ^ proximo_de(l,e) -> destino(e))", r_destino),
    ("R3 bloqueio", "Ve (fechada(e) -> bloqueada(e))", r_bloqueio),
    ("R4 acessibilidade", "Ve (precisa_acessibilidade ^ elevador_em_manutencao(e) -> inacessivel(e))", r_acessibilidade),
    ("R5 alerta", "Vp Ve (papel(p,e) ^ inacessivel(e) -> alerta(p,e))", r_alerta),
    ("R6 integração", "Vl1 Vl2 Ve (pertence(e, l1) ^ pertence(e, l2) ^ l1 != l2 -> integracao(e))", r_integracao),
    ("R7 linha paralisada", "Vl Ve (linha_paralisada(l) ^ pertence(e, l) -> bloqueada(e))", r_linha_paralisada)
]

def encadear_para_frente(fatos, regras, verbose=False):
    fatos = set(fatos)
    justificativas = {}
    while True:
        novos_na_rodada = set()
        for nome, formula, regra in regras:
            for fato in regra(fatos) - fatos:
                novos_na_rodada.add(fato)
                justificativas[fato] = nome
        if not novos_na_rodada: return fatos, justificativas
        fatos |= novos_na_rodada

def estacao_operacional(linha_paralisada, estacao_fechada):
    return (not linha_paralisada) and (not estacao_fechada)

def tabela_verdade_r7():
    print(" Linha Paralisada (P) | Estação Fechada (Q) | Operacional (~P ^ ~Q) ")
    print("-" * 68)
    for P, Q in product([True, False], repeat=2):
        print(f" {str(P):<20} | {str(Q):<19} | {estacao_operacional(P, Q)}")