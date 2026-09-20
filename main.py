# TEMPO_POR_TRECHO foi simulado como 2 minutos no guião original
TEMPO_POR_TRECHO = 2 
TEMPO_POR_BALDEACAO = 5 # Bónus: adicionar tempo extra por transbordo[cite: 1]

def planejar(pedido, fechadas=(), manutencao=(), paralisadas=(), algoritmo="BFS"):
    """
    Função central que une a lógica à busca em grafos.
    pedido: {"origem": (tipo, nome), "destino": (tipo, nome), "acessibilidade": bool}
    """
    # 1) Monta a base de conhecimento com o pedido e o cenário
    # Agora passamos as LINHAS e LOCAIS para criar os factos das 3 linhas
    fatos = fatos_base(LINHAS, LOCAIS)
    
    tipo_o, nome_o = pedido["origem"]
    tipo_d, nome_d = pedido["destino"]
    
    fatos.add(("usuario_esta_em", nome_o) if tipo_o == "local" else ("usuario_esta_na_estacao", nome_o))
    fatos.add(("usuario_quer_ir", nome_d) if tipo_d == "local" else ("usuario_quer_ir_estacao", nome_d))
    
    if pedido.get("acessibilidade"):
        fatos.add(("precisa_acessibilidade",))
        
    for e in fechadas:
        fatos.add(("fechada", e))
        
    for e in manutencao:
        fatos.add(("elevador_em_manutencao", e))
        
    # Integração da nova Regra 7 (Linha paralisada)
    for l in paralisadas:
        fatos.add(("linha_paralisada", l))

    # 2) Inferência lógica (O motor de inferência deduz os factos novos)[cite: 1]
    fatos, justificativas = encadear_para_frente(fatos, REGRAS)
    
    # Extrair os resultados da dedução
    origem = consultar(fatos, "origem")[0][0]
    destino = consultar(fatos, "destino")[0][0]
    bloqueadas = [e for (e,) in consultar(fatos, "bloqueada")]
    alertas = consultar(fatos, "alerta")
    
    # 3) Busca usando o que a lógica deduziu[cite: 1]
    buscar = bfs if algoritmo == "BFS" else dfs
    caminho, visitados = buscar(GRAFO, origem, destino, bloqueadas)
    
    # 4) NOVIDADE 2.0: Calcular as baldeações (transbordos) se houver um caminho
    lista_baldeacoes = []
    qtd_baldeacoes = 0
    tempo_total = None
    
    if caminho:
        # Chama a função que criou no linhas.py
        qtd_baldeacoes, lista_baldeacoes = contar_baldeacoes(caminho, LINHAS_DO_TRECHO)
        
        # Calcular tempo: 2 min por trecho + 5 min por baldeação
        tempo_total = ((len(caminho) - 1) * TEMPO_POR_TRECHO) + (qtd_baldeacoes * TEMPO_POR_BALDEACAO)

    # Devolve tudo num dicionário para o Narrador (LLM) e para a Interface
    return {
        "origem": origem,
        "destino": destino,
        "algoritmo": algoritmo,
        "caminho": caminho,
        "visitados": visitados,
        "bloqueadas": sorted(bloqueadas),
        "alertas": [f"{papel}: {e}" for papel, e in alertas],
        "paradas": len(caminho) - 1 if caminho else None,
        "baldeacoes": lista_baldeacoes,       # Adicionado para o R4 e R5
        "qtd_baldeacoes": qtd_baldeacoes,     # Adicionado para a interface
        "tempo_min": tempo_total,
        "regras_usadas": sorted(set(justificativas.values()))
    }