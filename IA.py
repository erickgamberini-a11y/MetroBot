# llm.py
import os
import json
import re
import unicodedata

from dotenv import load_dotenv
load_dotenv()

from linhas import TODAS_ESTACOES, LOCAIS


PROVEDOR = "groq" 
MODELO_GROQ = "llama-3.3-70b-versatile" 

def obter_chave_groq():
    chave = os.getenv("GROQ_API_KEY")
            
    return chave

def chamar_llm(mensagens, modo_json=False):
    if PROVEDOR == "groq":
        from groq import Groq
        cliente = Groq(api_key=obter_chave_groq())
        extras = {"response_format": {"type": "json_object"}} if modo_json else {}
        resposta = cliente.chat.completions.create(
            model=MODELO_GROQ, 
            messages=mensagens, 
            temperature=0, 
            **extras
        )
        return resposta.choices[0].message.content
    else:
        raise RuntimeError("Provedor LLM incorreto ou não configurado.")

def normalizar(texto):

    texto = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")

def resolver_nome(nome):
    if not nome: 
        return None
    alvo = normalizar(nome).strip()
    for estacao in TODAS_ESTACOES:
        if normalizar(estacao) == alvo: return ("estacao", estacao)
    for local in LOCAIS:
        if normalizar(local) == alvo: return ("local", local)
    return None

PROMPT_INTERPRETE = """Você é o módulo de INTERPRETAÇÃO do MetrôBot SP.
Sua única tarefa é transformar o pedido do passageiro em JSON.

Estações válidas: {estacoes}
Locais válidos: {locais}

Responda APENAS com um JSON neste formato:
{{"origem": "<nome exato de estação ou local, ou null>",
"destino": "<nome exato de estação ou local, ou null>",
"acessibilidade": <true ou false>}}

Regras: 
- Use SOMENTE nomes das listas acima, escritos exatamente como aparecem.
- acessibilidade é true se o passageiro mencionar cadeira de rodas, mobilidade reduzida, muletas, carrinho de bebê ou precisar de elevador.
Se não souber algum campo, use null. Nunca invente nomes."""

def interpretar_offline(texto):
    texto_min = texto.lower()
    texto_sem = normalizar(texto)
    candidatos = [(n, "estacao") for n in TODAS_ESTACOES] + [(n, "local") for n in LOCAIS]
    candidatos.sort(key=lambda c: len(c[0]), reverse=True)
    ocupado = [False] * len(texto_min)
    encontrados = []
    
    for nome, tipo in candidatos:
        buscas = [(texto_min, nome.lower())]
        if len(nome) > 4 and len(texto_sem) == len(texto_min):
            buscas.append((texto_sem, normalizar(nome)))
        for base, padrao in buscas:
            for m in re.finditer(r"(?<!\w)" + re.escape(padrao) + r"(?!\w)", base):
                if not any(ocupado[m.start():m.end()]):
                    encontrados.append((m.start(), nome))
                    for i in range(m.start(), m.end()): ocupado[i] = True
    encontrados.sort()
    palavras_acess = ["cadeira de rodas", "acessibilidade", "mobilidade", "muleta", "carrinho", "elevador"]
    
    return {
        "origem": encontrados[0][1] if len(encontrados) > 0 else None,
        "destino": encontrados[1][1] if len(encontrados) > 1 else None,
        "acessibilidade": any(p in texto_sem for p in palavras_acess)
    }

def interpretar_pedido(texto):
    sistema = PROMPT_INTERPRETE.format(
        estacoes=", ".join(TODAS_ESTACOES), 
        locais=", ".join(LOCAIS.keys())
    )
    
    try:
        resposta = chamar_llm([
            {"role": "system", "content": sistema},
            {"role": "user", "content": texto}
        ], modo_json=True)
        bruto = json.loads(resposta)
        fonte = PROVEDOR
    except Exception as erro:
        print(f"LLM indisponível ({erro}). Usando modo offline.")
        bruto = interpretar_offline(texto)
        fonte = "offline"
        
    origem = resolver_nome(bruto.get("origem"))
    destino = resolver_nome(bruto.get("destino"))
    
    if origem is None or destino is None:
        return None, f"Não entendi origem/destino (resposta bruta: {bruto})"
        
    pedido = {
        "origem": origem, 
        "destino": destino, 
        "acessibilidade": bool(bruto.get("acessibilidade"))
    }
    return pedido, f"Interpretado via {fonte}"


PROMPT_NARRADOR = """Você é o NARRADOR do MetrôBot SP. Explique a rota ao passageiro em português, em no máximo 4 frases curtas e simpáticas.
Use SOMENTE os dados do JSON. Não invente horários, linhas, estações ou atrações. 
Se caminho for null, explique que não há rota e cite as estações bloqueadas. 
CRÍTICO: Se houver 'baldeacoes' no JSON, explique claramente em qual estação o passageiro deve trocar de linha e para qual linha.
Se houver 'alertas', destaque-os."""

def narrar_offline(r):
    if r["caminho"] is None:
        return f"Não existe rota de {r['origem']} até {r['destino']} com as estações bloqueadas: {', '.join(r['bloqueadas'])}."
    
    texto = f"Embarque em {r['origem']} e siga até {r['destino']}: {r['paradas']} parada(s), cerca de {r['tempo_min']} minutos."
    if r['baldeacoes']:
        texto += " Baldeações: " + ", ".join([f"na {e} para a {l}" for e, l in r['baldeacoes']]) + "."
    if r["alertas"]:
        texto += " Atenção: " + ", ".join(r["alertas"]) + " (elevador em manutenção)."
    return texto

def narrar(resultado):
    dados = {k: resultado[k] for k in ("origem", "destino", "caminho", "paradas", "tempo_min", "bloqueadas", "alertas", "baldeacoes") if k in resultado}
    
    try:
        return chamar_llm([
            {"role": "system", "content": PROMPT_NARRADOR},
            {"role": "user", "content": json.dumps(dados, ensure_ascii=False)}
        ])
    except Exception as erro:
        return narrar_offline(resultado) + f" (narrador offline: {erro})"