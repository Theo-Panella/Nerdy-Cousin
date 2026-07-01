import re

def analisa_ip(logs):
    regex_failed = re.compile(r"Failed password for .*")
    regex_accepted = re.compile(r"Accepted password for .*")
    regex_invalid = re.compile(r"Invalid user .*|Failed password for invalid user .*")
    regex_closed = re.compile(r"Connection closed .*")
    regex_disconnect = re.compile(r"Received disconnect")

    #for result in logs:
    if regex_failed.search(logs):
        log_wrong_passwd_ip = re.search("Failed password for.* from (.*) port", logs)
        if log_wrong_passwd_ip:
            return log_wrong_passwd_ip.group(1)
    
    elif regex_closed.search(logs):
        log_connec_close = re.search(f"Connection closed by authenticating user.* (.*) port .*", logs)
        if log_connec_close:
            return log_connec_close.group(1)

    elif regex_disconnect.search(logs):
        log_Received_disconnect = re.search("Received disconnect from (.*) port .*", logs)
        if log_Received_disconnect:
            return log_Received_disconnect.group(1)
            
    elif regex_invalid.search(logs):
        log_invalid_user_ip = re.search("Invalid user.* from (.*) port", logs)
        if log_invalid_user_ip:
            return log_invalid_user_ip.group(1)
        
    elif regex_accepted.search(logs):
        log_successful_login_ip = re.search("Accepted password for.* from (.*) port", logs)
        if log_successful_login_ip:
            return log_successful_login_ip.group(1)