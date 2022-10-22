import re
import subprocess
import socket

def run_command(command: list[str]) -> str:
    try:
        raw_output = subprocess.run(command, stdout=subprocess.PIPE)
        return raw_output.stdout.decode('utf-8')
    except OSError:
        raise Exception(f'Error running command: {command}')

def get_client_net_details() -> dict[str:str]:
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    ip_config_output = run_command(['ipconfig', '/all'])
    dns_pattern = r"DNS Servers[ \.]+: ((?:[\d]{1,3}.){3}[\d]{1,3})"
    dns_servers = None
    if match := re.search(dns_pattern, ip_config_output):
        dns_servers = match.group(1)

    return {
        "hostname": hostname, 
        "ip": ip_address,
        "dns_server": dns_servers,
        }


if __name__ == '__main__':
    print(get_client_net_details())