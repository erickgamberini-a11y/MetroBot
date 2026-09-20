# llm.py
import os, json, re, unicodedata
from linhas import TODAS_ESTACOES, LOCAIS

PROVEDOR = "offline" # Troque para "groq" ou "ollama" se desejar ligar a API
MODELO_GROQ = "llama-3.3-70b-versatile"
MODELO_OLLAMA = "llama3.2"

def normalizar(texto):
    texto = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")

def resolver_nome(nome):
    if not nome: return None
    alvo = normalizar(nome).strip()
    for estacao in TODAS_ESTACOES:
        if normalizar(estacao) == alvo: return ("estacao", estacao)
    for local in LOCAIS:
        if normalizar(local) == alvo: return ("local", local)
    return None

PROMPT_INTERPRETE = """Você é o módulo de INTERPRETAÇÃO do MetrôBot SP.
Sua tarefa é transformar o pedido do passageiro em JSON.
Estações válidas: {estacoes}
Locais válidos: {locais}
Responda APENAS com um JSON neste formato:
{{"origem": "<nome exato de estação ou local, ou null>",
"destino": "<nome exato de estação ou local, ou null>",
"acessibilidade": <true ou false>}}
Regras: Use SOMENTE nomes das listas. acessibilidade é true se houver cadeiras de rodas, muletas, etc."""

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
    if PROVEDOR == "offline":
        bruto = interpretar_offline(texto)
        fonte = "offline"
    else:
        # Lógica omitida da API (Groq) para simplicidade offline
        bruto = interpretar_offline(texto)
        fonte = "offline"
        
    origem = resolver_nome(bruto.get("origem"))
    destino = resolver_nome(bruto.get("destino"))
    if origem is None or destino is None:
        return None, f"Não entendi origem/destino (resposta bruta: {bruto})"
    return {"origem": origem, "destino": destino, "acessibilidade": bool(bruto.get("acessibilidade"))}, f"Interpretado via {fonte}"

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
    return narrar_offline(resultado)