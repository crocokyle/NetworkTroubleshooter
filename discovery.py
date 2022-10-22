from endpoint import Endpoint
from utils import run_command, get_client_net_details

import re
from netaddr import IPAddress, AddrFormatError

def _parse_tracert(command_output:str) -> list[IPAddress]:
    route_pattern = r"over a maximum of 30 hops:\s+(.*)\nTrace complete."
    output = re.search(route_pattern, command_output, flags=re.MULTILINE|re.DOTALL).group(1)
    lines = output.splitlines()
    
    hops = []
    for line in lines:
        if line:
            dirty_ip = line.split()[-1]
            clean_ip = dirty_ip.replace('[', '').replace(']', '')
            try:
                hops.append(IPAddress(clean_ip))
            except AddrFormatError:
                raise Exception(f'Invalid IP address {clean_ip}')
    
    return hops

def get_internal_endpoints() -> list[IPAddress]:
    print(f'Running traceroute...')
    tracert_output = run_command(['tracert', '8.8.8.8'])
    hops = _parse_tracert(tracert_output)

    internal_ips = []
    for hop in hops:
        if hop.is_private():
            internal_ips.append(hop)

    return internal_ips
    
def get_localhost_ip() -> str:
    pass

if __name__ == '__main__':
    print(get_internal_endpoints())
