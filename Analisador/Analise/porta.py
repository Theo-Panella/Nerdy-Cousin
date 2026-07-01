import re
def analisa_porta(logs):
        
    regex_failed = re.compile(r"Failed password for .*")
    regex_accepted = re.compile(r"Accepted password for .*")
    regex_invalid = re.compile(r"Invalid user .*|Failed password for invalid user .*")
    regex_closed = re.compile(r"Connection closed .*")
    regex_disconnect = re.compile(r"Received disconnect")


    if regex_failed.search(logs):
        log_wrong_passwd_port = re.search("Failed password for.* port (.*) ssh2", logs)
        if log_wrong_passwd_port:
            return log_wrong_passwd_port.group(1)
        
    elif regex_closed.search(logs):
        log_connec_close = re.search(f"Connection closed by authenticating user.* port (.*)", logs)
        if log_connec_close:
            return log_connec_close.group(1)
        
    elif regex_disconnect.search(logs):
        log_Received_disconnect = re.search("Received disconnect from .* port (.*)", logs)
        if log_Received_disconnect:
            return log_Received_disconnect.group(1)
        
    elif regex_invalid.search(logs):
        log_invalid_user_port = re.search("Invalid user.* port (.*)", logs)
        if log_invalid_user_port:
            return log_invalid_user_port.group(1) 
        
    elif regex_accepted.search(logs):
        log_successful_login_port = re.search("Accepted password for.* port (.*) ssh2", logs)
        if log_successful_login_port:
            return log_successful_login_port.group(1)