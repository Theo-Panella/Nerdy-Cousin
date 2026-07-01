import re
from Analise.contexto import analisar_contexto

def analisa_user(logs):
    regex_failed = re.compile(r"Failed password for .*")
    regex_accepted = re.compile(r"Accepted password for .*")
    regex_invalid = re.compile(r"Invalid user .*|Failed password for invalid user .*")
    regex_closed = re.compile(r"Connection closed .*")
    regex_disconnect = re.compile(r"Received disconnect")

    #for result in logs:
    if regex_failed.search(logs):
        log_wrong_passwd = re.search("Failed password for (.*) from", logs)
        #print(log_wrong_passwd)
        if log_wrong_passwd:
            return log_wrong_passwd.group(1)
        
    elif regex_closed.search(logs):
        log_connec_close = re.search("Connection closed by authenticating user (.*) .* port .*", logs)
        #print(log_connec_close)
        if log_connec_close:
            return log_connec_close.group(1)
    
    elif regex_disconnect.search(logs):
        log_Received_disconnect = re.search("Received disconnect from .* port .* disconnected by user (.*)", logs)
        if log_Received_disconnect:
            return log_Received_disconnect.group(1)
        
    elif regex_invalid.search(logs):
        log_invalid_user = re.search("Invalid user (.*) from .*", logs)
        #print("Failed login attempt for invalid user:", log_invalid_user)
        if log_invalid_user:
            return log_invalid_user.group(1)
        
    elif regex_accepted.search(logs):
        log_valid_user = re.search(f"Accepted password for (.*) from", logs)
        #print("Successful login for user:", log_valid_user)
        return log_valid_user.group(1)