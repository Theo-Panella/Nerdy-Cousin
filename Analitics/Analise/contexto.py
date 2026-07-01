import re

# Compilação prévia melhora performance
regex_failed = re.compile(r"Failed password for")
regex_accepted = re.compile(r"Accepted password for")
regex_invalid = re.compile(r"Invalid user|Failed password for invalid user")
regex_closed = re.compile(r"Connection closed|Received disconnect")

def analisar_contexto(linha_log):
    
    if regex_invalid.search(linha_log):
        return "usuario inexistente"
    
    elif regex_failed.search(linha_log):
        return "Acesso Negado"
    
    elif regex_accepted.search(linha_log):
        return "Acesso aceito"
    
    elif regex_closed.search(linha_log):
        return "Conexão fechada"

    else:
        return "Evento desconhecido"