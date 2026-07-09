#====================================================================================
# Centralizador - API de recepcao de logs
#
# API simples baseada em FastAPI (funciona em Windows e Linux via uvicorn).
# Recebe os logs enviados pelo Minimim via POST e os armazena/registra.
#
# Executar:
#   uvicorn Centralizador.central:app --host 0.0.0.0 --port 8000 --reload
#====================================================================================
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel

#====================================================================================
# Configuracao
arquivo_de_logs = r".\Material\logs_centralizado.txt"
#====================================================================================


#====================================================================================
# Modelo do corpo da requisicao.
# O Minimim envia {"log": "<linha>"}; os demais campos sao opcionais.
class LogRecebido(BaseModel):
    log: str
    servico: str | None = None
    tipo: str | None = None
#====================================================================================


app = FastAPI(title="Centralizador de Logs", version="1.0.0")


#====================================================================================
# Recepcao dos logs
@app.post("/")
def receber_log(entrada: LogRecebido):
    
    prioridade = 0
    fila = ''
    momento = datetime.now(timezone.utc).isoformat()

    # Monta a linha de registro com o horario de recebimento e a origem.

    peso_servico = {"Flask": 3, "Nginx": 2}
    peso_por_tipo = {
        "admin_access_failed": 7,
        "recon_by_trying_access_inexistent_page": 3,
        "normal_access_failed": 3,
        "admin_access_accepted": 1,
        "normal_access_accepted": 1,
    }

    prioridade = peso_servico.get(entrada.servico, 0) + peso_por_tipo.get(entrada.tipo, 0)

    match prioridade:
        case int(prioridade) if prioridade <= 3:
            fila = "Baixa"
        case int(prioridade) if prioridade > 3 and prioridade <= 5:
            fila = "Baixa_media"
        case int(prioridade) if prioridade > 5 and prioridade <= 7:
            fila = "média"
        case int(prioridade) if prioridade >= 8 and prioridade <= 9:
            fila = "média_alta"      
        case int(prioridade) if prioridade > 10:
            fila = "alta"    

    origem = f"[{entrada.servico or '-'}/{entrada.tipo or '-'}/{fila}]"
    linha = f"{momento} {origem}"

    # Persiste em arquivo (append) alem de imprimir no console.
    with open(arquivo_de_logs, "a", encoding="utf-8") as arquivo:
        arquivo.write(linha + "\n")
    print(f"Log recebido: {linha}")

    return {"status": "ok", "recebido_em": momento}
#====================================================================================


#====================================================================================
# Healthcheck simples
@app.get("/")
def healthcheck():
    return {"status": "online", "servico": "Centralizador de Logs"}
#====================================================================================
