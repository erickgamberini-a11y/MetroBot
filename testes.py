# ===== TESTES OBRIGATÓRIOS (R6) =====

def rodar_testes():
    # 1. Validar total de estações (52 únicas nas 3 linhas)
    assert len(GRAFO) == 52, f"Erro: O grafo tem {len(GRAFO)} estações em vez de 52."
    
    # 2. Caso 1: Tucuruvi -> Corinthians-Itaquera (Normal)
    # Esperado: 22 paradas, 1 baldeação (na Sé)
    r1 = planejar({"origem": ("estacao", "Tucuruvi"), "destino": ("estacao", "Corinthians-Itaquera")})
    assert r1['paradas'] == 22
    assert len(r1['baldeacoes']) == 1 and r1['baldeacoes'][0][0] == 'Sé'
    
    # 3. Caso 2: Vila Madalena -> Jabaquara (Normal)
    # Esperado: 14 paradas, 1 baldeação (Paraíso ou Ana Rosa)
    r2 = planejar({"origem": ("estacao", "Vila Madalena"), "destino": ("estacao", "Jabaquara")})
    assert r2['paradas'] == 14
    assert len(r2['baldeacoes']) == 1
    assert r2['baldeacoes'][0][0] in ['Paraíso', 'Ana Rosa']
    
    # 4. Caso 4: Tucuruvi -> Brás (Sé fechada)
    # Esperado: Sem rota
    r4 = planejar({"origem": ("estacao", "Tucuruvi"), "destino": ("estacao", "Brás")}, fechadas=["Sé"])
    assert r4['caminho'] is None
    
    # 5. Caso 5: Vila Madalena -> Jabaquara (Paraíso fechada)
    # Esperado: Sem rota (Linha 2 cortada no Paraíso)
    r5 = planejar({"origem": ("estacao", "Vila Madalena"), "destino": ("estacao", "Jabaquara")}, fechadas=["Paraíso"])
    assert r5['caminho'] is None
    
    # 6. Caso 6: Vila Prudente -> Jabaquara (Paraíso fechada)
    # Esperado: 13 paradas, via Ana Rosa (desvio)
    r6 = planejar({"origem": ("estacao", "Vila Prudente"), "destino": ("estacao", "Jabaquara")}, fechadas=["Paraíso"])
    assert r6['paradas'] == 13
    assert 'Ana Rosa' in r6['caminho']
    assert 'Paraíso' not in r6['caminho']

    print("✅ Todos os testes obrigatórios passaram!")

# Execute esta função para validar o seu progresso
# rodar_testes()