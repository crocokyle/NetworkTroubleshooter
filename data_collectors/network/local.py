# Local imports
from utils.operating_system import legacy_run_command
from data_collectors.abstract import DataCollector

# 3rd party imports
import psutil
import re
import socket

class WindowsDataCollector(DataCollector):
    def __init__(self):
        super().__init__()
        
    @staticmethod
    def _get_connected_interface(local_ip_address: str) -> str:
        interfaces = psutil.net_if_addrs()    
        for key in interfaces:
            for snic in interfaces[key]:
                if snic.address == local_ip_address:
                    return key

    @staticmethod
    def _parse_ipconfig_property(property: str, cmd_output: str) -> str:
        property_value = None
        property_pattern = re.escape(property) + "[ \.]+: ((?:[\d]{1,3}.){3}[\d]{1,3})"
        if match := re.search(property_pattern, cmd_output):
            property_value = match.group(1)

        return property_value

    def get_client_net_info(self) -> None:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        ip_config_output = legacy_run_command(['ipconfig', '/all'])

        self.data.Network.HOSTNAME.val = hostname
        self.data.Network.CONNECTED_IP.val = ip_address
        self.data.Network.CONNECTED_INTERFACE.val = self._get_connected_interface(ip_address)
        self.data.Network.DNS_SERVER.val = self._parse_ipconfig_property("DNS Servers", ip_config_output)
        self.data.Network.GATEWAY.val = self._parse_ipconfig_property("Default Gateway", ip_config_output)
        self.data.Network.DHCP_SERVER.val = self._parse_ipconfig_property("DHCP Server", ip_config_output)

    def run(self):
        self.get_client_net_info()
        super().run()

if __name__ == '__main__':
    local_dc = WindowsDataCollector()
    local_dc.run()
    
    for fact in local_dc.data.Network:
        print("===========================")
        print(f'Fact description: {fact.description}')
        print(f'Value: {fact.val}')
        print("===========================\n")