# Nerdy-better

Mini-SIEM em Python para **coleta, filtragem e análise de logs de segurança** de um serviço
web (Flask). O sistema observa os logs de um host, filtra os eventos relevantes, classifica
sua criticidade e (na visão-alvo) os disponibiliza para um dashboard.

> Projeto acadêmico, em desenvolvimento. Alguns estágios do pipeline já funcionam de forma
> isolada; outros ainda são esqueleto conceitual (ver [Status](#status)).

---

## Arquitetura

O projeto é um pipeline em estágios, um por pasta:

```
Host Server ──► Coleta (Minimim) ──► Centralizador ──► Servidor de Fila ──► Servidor de Análise ──► Dashboard
                     │                     │                  │                     │
               filtra enquanto       recebe e classifica   Baixa / Média /   parse → análise →
               coleta (pré-filtro)   em prioridades        Alta prioridade   criticidade → índice
```

| Estágio | Pasta | Responsabilidade |
|---|---|---|
| Coleta + pré-filtro | [`Minimim/`](Minimim/) | Observa o arquivo de log e filtra linhas por regras configuráveis, ordenadas por **especificidade** (só organiza a pré-análise/roteamento). |
| Centralização | [`Centralizador/`](Centralizador/) | Recebe a coleta, classifica em prioridades e envia para a fila correspondente. |
| Fila | *(planejado)* | Filas por prioridade (Baixa/Média/Alta) desacoplando coleta e análise. |
| Análise | [`Analisador/`](Analisador/) | Quebra o log, analisa cada campo e atribui um **nível de criticidade**. |
| Visualização | [`Dashboard/`](Dashboard/) | Exibição dos eventos analisados. |
| Dados/saídas | [`Material/`](Material/) | Logs de entrada e artefatos gerados (YAML de resultados). |

> **Especificidade × Criticidade** são conceitos distintos: a *especificidade* (no Minimim)
> é rasa e serve para filtrar/rotear a linha crua; a *criticidade* (no Analisador) é profunda,
> derivada da quebra e análise dos campos do log.

---

## Estrutura do repositório

```
Minimim/
  MiniMim.py        # coletor: watchdog + pré-filtro por especificidade
  config.yaml       # regras de filtragem por serviço (padrão + especificidade)
Analisador/
  main_Analitics.py # orquestra a análise e agrega os eventos
  Analise/          # extratores de campo, um por item quebrado do log
    IP.py  User.py  Servidor.py  porta.py  pid.py  contexto.py
Centralizador/central.py    # (esqueleto)
Dashboard/main_dashboard.py # (esqueleto)
Material/          # logs de entrada e saídas geradas
requirements.txt
```

---

## Requisitos

- Python 3.11+
- Dependências em [`requirements.txt`](requirements.txt) (Flask, PyYAML, watchdog, requests, …)

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

---

## Como usar

Execute os comandos **a partir da raiz do projeto** (os caminhos são relativos a ela).

### Coletor (Minimim)
Observa o arquivo de log e aplica o pré-filtro definido no `config.yaml`:

```bash
python Minimim/MiniMim.py
```

### Analisador
Lê os logs, quebra cada linha, agrega os eventos e gera o YAML de resultados:

```bash
python Analisador/main_Analitics.py
```

### Centralizador (API Falcon)
Sobe a API Falcon do Centralizador via gunicorn:

```bash
gunicorn Centralizador.central:app
```

---

## Configuração do pré-filtro (`Minimim/config.yaml`)

As regras são organizadas por **serviço**; cada regra tem um `padrao` (regex) e uma
`especificidade`. O pré-filtro avalia da maior para a menor especificidade e para no
primeiro match (o mais específico vence):

```yaml
Flask:
    admin_access_failed:
        padrao: ' flask\[\d+\]: Failed password for admin from .*'
        especificidade: 10
    normal_access_failed:
        padrao: ' flask\[\d+\]: Failed password for .*'
        especificidade: 1
```

Apenas serviços listados em `lista_de_servico` (dentro de `MiniMim.py`) são processados.

---

## Status

| Componente | Estado |
|---|---|
| Coletor + pré-filtro por especificidade | ✅ Funcional |
| Extratores de campo (IP, usuário, porta, PID, contexto, servidor) | ✅ Funcional |
| Agregação de eventos | ✅ Funcional |
| Classificação de criticidade (correlação: volume + falha→sucesso) | 🚧 Planejado |
| Centralizador / Filas por prioridade | 🚧 Planejado |
| Indexação / Dashboard | 🚧 Planejado |

---

## Notas

- A pasta `.venv/` e caches `__pycache__/` são ignorados via [`.gitignore`](.gitignore).
- Os artefatos de saída ficam em [`Material/`](Material/).
