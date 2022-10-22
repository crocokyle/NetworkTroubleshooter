import re
import socket
import time
from PyQt5.QtCore import QProcess


from netaddr import IPAddress

def _get_completed_stdout(process: QProcess) -> str:
    return process.readAllStandardOutput().data().decode()

def run_command(command: list[str], console_process: QProcess) -> str:
    try:
        console_process.setProgram(command[0])
        if len(command) > 1:
            console_process.setArguments(command[1:])
        while not console_process.finished():
            time.sleep(1)
        raw_output = console_process.readAllStandardOutput().data().decode()
        return raw_output
    except:
        raise Exception(f'Error running command: {command}')

def is_same_subnet(ip1: IPAddress, ip2: IPAddress) -> bool:
    if ip1.words[0:3] == ip2.words[0:3]:
        return True
    return False

def get_client_net_info() -> dict[str:str]:
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    ip_config_output = run_command(['ipconfig', '/all'])
    dns_pattern = r"DNS Servers[ \.]+: ((?:[\d]{1,3}.){3}[\d]{1,3})"
    dns_servers = None
    if match := re.search(dns_pattern, ip_config_output):
        dns_servers = match.group(1)

    return {
        #"gateway": gateway,
        "hostname": hostname, 
        "ip": ip_address,
        "dns_server": dns_servers,
        }


if __name__ == '__main__':
    net_details = get_client_net_info()
    print(net_details)