# 🚇 MetrôBot SP 2.0 - Agente Neuro-Simbólico de Roteamento

Este projeto é a evolução do MetrôBot (versão 2.0), desenvolvido como desafio prático da disciplina de Inteligência Artificial e Machine Learning. O sistema atua como um agente autônomo focado em mobilidade urbana, capaz de interpretar linguagem natural, deduzir restrições lógicas e traçar a melhor rota entre as Linhas 1-Azul, 2-Verde e 3-Vermelha do Metrô de São Paulo.

## 🧠 Arquitetura do Sistema

O MetrôBot utiliza o paradigma da **IA Neuro-Simbólica**, combinando três pilares essenciais da Inteligência Artificial:

1. **Processamento de Linguagem Natural (LLMs):** Modelos de linguagem (Llama via API Groq) atuam como os "olhos" e a "boca" do agente[cite: 1]. Um **Intérprete** transforma o pedido caótico do utilizador num formato JSON estruturado, lidando com sinônimos e intenções de acessibilidade. Um **Narrador** traduz o trajeto matemático gerado pelo sistema numa explicação simpática e em português claro[cite: 1].
2. **Lógica de Primeira Ordem (Motor de Inferência):** Antes da rota ser calculada, um motor de encadeamento para a frente (*forward chaining*) cruza os dados do pedido com as regras do mundo[cite: 1]. Ele deduz a estação mais próxima (R1 e R2), bloqueia estações fechadas (R3) ou vias inteiras paralisadas (R7), averigua necessidades de elevadores (R4) e descobre automaticamente onde ocorrem as integrações (R6)[cite: 1].
3. **Busca Heurística em Grafos (BFS e DFS):** Com as restrições lógicas definidas, os algoritmos clássicos percorrem um grafo bidirecional contendo 52 estações[cite: 1]. A Busca em Largura (BFS) assegura o caminho com menor número de paradas, enquanto o sistema registra onde o passageiro necessitará fazer baldeações (transbordos)[cite: 1].

## ✨ Principais Funcionalidades

* **Cobertura Multi-Linhas:** Rotas integradas cobrindo 52 estações únicas das Linhas Azul, Verde e Vermelha, com transbordos automáticos mapeados na Sé, Paraíso e Ana Rosa[cite: 1].
* **Validação de NLP Avançada (Guardrails):** A entrada em texto livre suporta apelidos e omissões (ex: "HC", "Itaquera"), contendo travas de segurança para evitar alucinações (nomes que não existem) ou forçar um *fallback* robusto *offline* caso a API de linguagem fique inoperante[cite: 1].
* **Painel Gráfico Dinâmico:** Interface desenvolvida com `ipywidgets`, exibindo um *render* visual em HTML com as cores oficiais das linhas e marcadores de estado (bloqueada, visitada, rota)[cite: 1].
* **Suite de Testes Automatizados:** Cobertura de 6 cenários de uso obrigatórios (testes de mesa), garantindo a robustez do cálculo de trajetos sob diferentes anomalias (ex: estação de integração fechada)[cite: 1].

## 📂 Estrutura do Projeto

O código, inicialmente um bloco monolítico, foi refatorado seguindo as melhores práticas de engenharia de software, separando responsabilidades:

* `dados.py`: Armazena as listas de estações, locais de referência, construção da lista de adjacências e cálculo de baldeações.
* `busca.py`: Isola as lógicas puras de exploração em árvore/grafo (`bfs` e `dfs`).
* `logica.py`: Gerencia a Base de Conhecimento, Fatos e Regras em formato de tuplas, executando o motor de encadeamento para a frente.
* `llm.py`: Trata a injeção de *prompts*, comunicação com a API (via pacote `groq` e `.env`) e modos de segurança *offline*.
* `main.py`: O "cérebro" orquestrador, onde reside a função `planejar()` e o executor dos testes automatizados.
* `interface.ipynb`: O notebook Jupyter encarregado de desenhar e orquestrar os controles visuais da aplicação.

## 🚀 Como Instalar e Rodar

**1. Pré-requisitos e Dependências**
Certifique-se de ter o Python 3.10 ou superior. No terminal, instale os requisitos:
```bash
pip install groq python-dotenv ipywidgets
```

**2. Gestão de Chaves (Segurança)**
O projeto não possui chaves de API expostas no código. Crie um arquivo exatamente com o nome .env na raiz da pasta e adicione as suas credenciais:
```Plaintext
GROQ_API_KEY=gsk_sua_chave_de_acesso_aqui
```

**3. Teste de Validação (CLI)**
Para aferir a integridade da árvore de decisão e motor de busca, execute os testes unitários via linha de comando:
```Bash
python main.py
```
(Saída esperada: "✅ Todos os testes obrigatórios passaram com sucesso!")

**4. Interface de Usuário (GUI)**
Para interagir com o bot visualmente, inicie o arquivo interface.ipynb dentro de um ambiente Jupyter (como o VS Code ou JupyterLab) e execute a célula integralmente.


## Autor: Erick Ventura Gamberini - 03099001