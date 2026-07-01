import re
import yaml
from Analise.IP import analisa_ip
from Analise.porta import analisa_porta
from Analise.User import analisa_user
from Analise.pid import analisa_pid
from Analise.Servidor import analisa_servidor
from Analise.contexto import analisar_contexto

# Padrão de Analise
# Data | Hora | IP de requisicao | IP de Destino | Serviço | Porta | Protocolo | Username | Hostname
# Tipo de log: Erro, acesso, alteração, requisição

# Variavel de abertura do arquivo de logs
log_file = open('Material/logs.txt', 'r')

# Leitura de linha dentro de uma array, cada linha é um index da array
logs = log_file.readlines() 
data = {}
eventos_agregados = {}

# --------------------------------------------------------------------------------------------------------------------
# Bloco de analise geral
# --------------------------------------------------------------------------------------------------------------------

def analisa_geral(logs):
        result = {
            "Usario": analisa_user(logs),
            "Endereco Servidor": analisa_servidor(logs),
            "IP de Origem": analisa_ip(logs),
            "porta de Conexao": analisa_porta(logs),
            "PID:" : analisa_pid(logs),
            "Contexto": analisar_contexto(logs)
        }

        return result
        

for log in logs:
    analise_por_campo = analisa_geral(log)

    usuario = analise_por_campo["Usario"]
    ip_origem = analise_por_campo["IP de Origem"]
    contexto = analise_por_campo["Contexto"]
    endereco_servidor = analise_por_campo["Endereco Servidor"]
    porta = analise_por_campo["porta de Conexao"]
    pid = analise_por_campo["PID:"]

    # ----------------------------------------
    # Chave principal de agregação
    # ----------------------------------------
    chave_evento = (usuario, ip_origem, contexto, endereco_servidor)

    if chave_evento not in eventos_agregados:
        eventos_agregados[chave_evento] = {
            "Usario": usuario,
            "Endereco Servidor": endereco_servidor,
            "IP de Origem": ip_origem,
            "Resumo do Log": contexto,
            "Tentativas": 1,
            "Portas": [porta],
            "PIDs": [pid]
        }
    else:
        eventos_agregados[chave_evento]["Tentativas"] += 1

        # Adiciona porta apenas se for diferente
        if porta not in eventos_agregados[chave_evento]["Portas"]:
            eventos_agregados[chave_evento]["Portas"].append(porta)

        # Mesmo critério para PID
        if pid not in eventos_agregados[chave_evento]["PIDs"]:
            eventos_agregados[chave_evento]["PIDs"].append(pid)


# ----------------------------------------
# Aplicar criticidade após agregação
# ----------------------------------------

for i, (chave, evento) in enumerate(eventos_agregados.items()):
    usuario, ip_origem, contexto, endereco_servidor = chave

    data[i] = evento


with open("Material/file.yaml", "w") as file:
    yaml.dump(data, file)