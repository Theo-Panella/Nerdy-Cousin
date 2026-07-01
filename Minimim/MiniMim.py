#====================================================================================
import time
import re
import yaml
from collections import deque
from watchdog.events import FileSystemEvent, FileSystemEventHandler,FileModifiedEvent
from watchdog.observers import Observer
#====================================================================================


#====================================================================================
# Variaveis Globais
lista_de_servico = ['Flask']
caminho_de_configuracao = ".\Minimim\config.yaml"
caminho_de_log = '.\\Material\\logs_colector.txt'
#====================================================================================


#====================================================================================
# Abre o arquivo de Configuracao e compila para melhor desempenho
# Abre regras individualmente, tem mais processamento na primeira rodagem por compilar
# todas as configurações inicialmente
with open(caminho_de_configuracao, 'r') as arquivo_de_configuracao_puro:
    configuracao = yaml.safe_load(arquivo_de_configuracao_puro)

regras = {
    servico: {
        tipo: re.compile(padrao)
        for tipo, padrao in padroes.items()
    }
    for servico, padroes in configuracao.items()
}
#====================================================================================


#====================================================================================
# Funcao de pre_Filtro do Flask
def flask_pre_filter(ultimas_linhas,regras):
    # Pega cada linha da ultima linha lida, default = 1
    for cada_linha in ultimas_linhas:
        ''' Pega cada serviço e seu padrao. 
        EX: Servico: 
                PadraoA: "Valor"
                PadraoB: "Valor"
                ...
        '''
        for servico, padrao in regras.items():
            if servico not in lista_de_servico:
                continue
            ''' Pega cada padrao (nome_padrao) e seu compile (str_padrao). 
                EX:
                        (PadraoA) nome_padrao: "str_padrao"
                        (PadraoB) nome_padrao: "str_padrao"
                        ...
                '''
            for nome_padrao, padrao_compilado  in padrao.items():
                # Verifica se atende os padrões daquele servico
                if padrao_compilado.search(cada_linha.strip()):
                    #envio_para_API(cada_linha.strip())
                    print(f'Log do servico {servico} e Tipo {nome_padrao} encontrado, aplicando pre-filtro do {servico}: {nome_padrao}')
                    #with open("Colector/minimim.txt", "a") as file:
                    #    file.write(cada_linha.strip() + "\n")

                    #print(f'Log de Acordo com a configuração encontrado ')
# Todo o PRE-FILTRO, precisa de uma função com essa mesma logica, 
#====================================================================================

#====================================================================================
# Envio do log para API
def envio_para_API(log):
    # Aqui você pode implementar a lógica para enviar o log para a API
    # Por exemplo, usando a biblioteca requests para fazer uma requisição POST
    import requests

    url = "http://sua-api-endpoint.com/logs"  # Substitua pelo endpoint da sua API
    headers = {"Content-Type": "application/json"}
    data = {"log": log}  # Você pode ajustar os dados conforme necessário

    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            print("Log enviado para servidor de analise")
        else:
            print(f"Falha ao enviar log. Status code: {response.status_code}")
    except Exception as e:
        print(f"Erro ao enviar log: {e}")


#====================================================================================
# Classe evento do Watchdog
class MyEventHandler(FileSystemEventHandler):
    def __init__(self):
        self._pos = 0          # Posicao inicial (Na primeira vez rodando faz ingestão inicial e depois continua apartir da ultima)

    def on_any_event(self, event: FileSystemEvent) -> None:
        if event.src_path == caminho_de_log and event.event_type == "modified":
            #print("Nova tentativa de Login detectada")
            #print("Analisando log...")
            with open(caminho_de_log, "r", encoding="utf-8") as f:
                #ultimas_linhas = deque(f, maxlen=quantidade_de_ultimas_linhas)
                f.seek(self._pos)
                novas_linhas = f.readlines()
                self._pos = f.tell()
                flask_pre_filter(novas_linhas,regras)
#====================================================================================


#====================================================================================
#Chama evento e mantem em loop
if __name__ == "__main__":
    event_handler = MyEventHandler()
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=True)
    observer.start()
    print("Analisando log...")
    try:    
        while True:
            time.sleep(2)
    finally:
        observer.stop()
        observer.join()
#====================================================================================