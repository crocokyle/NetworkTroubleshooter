from endpoint import Endpoint
from utils import is_same_subnet, run_command, get_client_net_info

import re
from netaddr import IPAddress, AddrFormatError
from PyQt5.QtCore import QProcess


def _parse_tracert(command_output:str) -> list[IPAddress]:
    route_pattern = r"over a maximum of 30 hops:\s+(.*)\nTrace complete."
    output = re.search(route_pattern, command_output, flags=re.MULTILINE|re.DOTALL).group(1)
    lines = output.splitlines()
    
    hops = []
    for line in lines:
        if line:
            ip_field = line.split()[-1].replace('[', '').replace(']', '')
            if re.match(r'(?:[0-9]{1,3}\.){3}[0-9]{1,3}', ip_field):
                try:
                    hops.append(IPAddress(ip_field))
                except AddrFormatError:
                    raise Exception(f'Invalid IP address {ip_field}')
    
    return hops

def get_private_ips(console_process: QProcess) -> list[IPAddress]:
    tracert_output = run_command(['tracert', '8.8.8.8'], console_process)
    hops = _parse_tracert(tracert_output)
    internal_ips = []
    for hop in hops:
        if hop.is_private():
            internal_ips.append(hop)

    return internal_ips

def get_internal_endpoints(console_process: QProcess) -> list[Endpoint]:
    private_ips: list[IPAddress] = get_private_ips(console_process)
    client_info:dict[str:str] = get_client_net_info()

    for ip in private_ips:
        if is_same_subnet(ip, client_info.get('ip')):
            router_endpoint = Endpoint('router', ip)
    
def get_localhost_ip() -> str:
    pass

if __name__ == '__main__':
    print(get_internal_endpoints())
