# main.py
from linhas import LINHAS, LOCAIS, GRAFO, LINHAS_DO_TRECHO, TODAS_ESTACOES, contar_baldeacoes
from logica import fatos_base, encadear_para_frente, REGRAS, consultar
from busca import bfs, dfs
from IA import interpretar_pedido, narrar

TEMPO_POR_TRECHO = 2
TEMPO_POR_BALDEACAO = 5

def planejar(pedido, fechadas=(), manutencao=(), paralisadas=(), algoritmo="BFS"):
    fatos = fatos_base(LINHAS, LOCAIS)
    tipo_o, nome_o = pedido["origem"]
    tipo_d, nome_d = pedido["destino"]
    
    fatos.add(("usuario_esta_em", nome_o) if tipo_o == "local" else ("usuario_esta_na_estacao", nome_o))
    fatos.add(("usuario_quer_ir", nome_d) if tipo_d == "local" else ("usuario_quer_ir_estacao", nome_d))
    
    if pedido.get("acessibilidade"): fatos.add(("precisa_acessibilidade",))
    for e in fechadas: fatos.add(("fechada", e))
    for e in manutencao: fatos.add(("elevador_em_manutencao", e))
    for l in paralisadas: fatos.add(("linha_paralisada", l))

    fatos, justificativas = encadear_para_frente(fatos, REGRAS)
    
    origens_val = consultar(fatos, "origem")
    destinos_val = consultar(fatos, "destino")
    origem = origens_val[0][0] if origens_val else None
    destino = destinos_val[0][0] if destinos_val else None
    
    bloqueadas = [e for (e,) in consultar(fatos, "bloqueada")]
    alertas = consultar(fatos, "alerta")
    
    buscar = bfs if algoritmo == "BFS" else dfs
    caminho, visitados = buscar(GRAFO, origem, destino, bloqueadas) if origem and destino else (None, [])
    
    lista_baldeacoes = []
    qtd_baldeacoes = 0
    tempo_total = None
    
    if caminho:
        qtd_baldeacoes, lista_baldeacoes = contar_baldeacoes(caminho, LINHAS_DO_TRECHO)
        tempo_total = ((len(caminho) - 1) * TEMPO_POR_TRECHO) + (qtd_baldeacoes * TEMPO_POR_BALDEACAO)

    return {
        "origem": origem, "destino": destino, "algoritmo": algoritmo,
        "caminho": caminho, "visitados": visitados, "bloqueadas": sorted(bloqueadas),
        "alertas": [f"{papel}: {e}" for papel, e in alertas],
        "paradas": len(caminho) - 1 if caminho else None,
        "baldeacoes": lista_baldeacoes, "qtd_baldeacoes": qtd_baldeacoes,
        "tempo_min": tempo_total, "regras_usadas": sorted(set(justificativas.values()))
    }

def rodar_testes():
    print("Iniciando testes...")
    assert len(GRAFO) == 52, f"Erro: O grafo tem {len(GRAFO)} estações em vez de 52."
    
    r1 = planejar({"origem": ("estacao", "Tucuruvi"), "destino": ("estacao", "Corinthians-Itaquera")})
    assert r1['paradas'] == 22, f"Erro no Caso 1: Paradas = {r1['paradas']}"
    assert len(r1['baldeacoes']) == 1 and r1['baldeacoes'][0][0] == 'Sé'
    
    r2 = planejar({"origem": ("estacao", "Vila Madalena"), "destino": ("estacao", "Jabaquara")})
    assert r2['paradas'] == 14
    assert len(r2['baldeacoes']) == 1 and r2['baldeacoes'][0][0] in ['Paraíso', 'Ana Rosa']
    
    r4 = planejar({"origem": ("estacao", "Tucuruvi"), "destino": ("estacao", "Brás")}, fechadas=["Sé"])
    assert r4['caminho'] is None
    
    r5 = planejar({"origem": ("estacao", "Vila Madalena"), "destino": ("estacao", "Jabaquara")}, fechadas=["Paraíso"])
    assert r5['caminho'] is None
    
    r6 = planejar({"origem": ("estacao", "Vila Prudente"), "destino": ("estacao", "Jabaquara")}, fechadas=["Paraíso"])
    assert r6['paradas'] == 13
    assert 'Ana Rosa' in r6['caminho'] and 'Paraíso' not in r6['caminho']

    print("✅ Todos os testes obrigatórios passaram com sucesso!")

if __name__ == "__main__":
    rodar_testes()