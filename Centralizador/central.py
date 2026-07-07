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
# Path(__file__).resolve() garante caminho absoluto correto em qualquer SO.
ARQUIVO_DE_LOGS = Path(__file__).resolve().parent / "Material/logs_recebidos.txt"
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
    momento = datetime.now(timezone.utc).isoformat()

    # Monta a linha de registro com o horario de recebimento e a origem.
    origem = f"[{entrada.servico or '-'}/{entrada.tipo or '-'}]"
    linha = f"{momento} {origem} {entrada.log}"

    # Persiste em arquivo (append) alem de imprimir no console.
    with open(ARQUIVO_DE_LOGS, "a", encoding="utf-8") as arquivo:
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
