# Local imports
from utils.operating_system import legacy_run_command

# 3rd party imports
import psutil
import re
import socket

def _get_connected_interface(local_ip_address: str) -> str:
    interfaces = psutil.net_if_addrs()    
    for key in interfaces:
        for snic in interfaces[key]:
            if snic.address == local_ip_address:
                return key

def _parse_ipconfig_property(property: str, cmd_output: str) -> str:
        property_value = None
        property_pattern = re.escape(property) + "[ \.]+: ((?:[\d]{1,3}.){3}[\d]{1,3})"
        if match := re.search(property_pattern, cmd_output):
            property_value = match.group(1)

        return property_value

def get_client_net_info() -> dict[str:str]:
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    ip_config_output = legacy_run_command(['ipconfig', '/all'])

    return {
        "hostname": hostname, 
        "ip": ip_address,
        "connected_interface": _get_connected_interface(ip_address),
        "dns_server": _parse_ipconfig_property("DNS Servers", ip_config_output),
        "gateway": _parse_ipconfig_property("Default Gateway", ip_config_output),
        "dhcp_server": _parse_ipconfig_property("DHCP Server", ip_config_output),
        }

if __name__ == '__main__':
    net_details = get_client_net_info()
    print(net_details)