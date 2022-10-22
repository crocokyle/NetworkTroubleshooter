# Local imports
from utils.operating_system import legacy_run_command
from data_collectors.interface import DataCollector

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

        self.data.network.hostname = hostname
        self.data.network.connected_ip = ip_address
        self.data.network.connected_interface = self._get_connected_interface(ip_address)
        self.data.network.dns_server = self._parse_ipconfig_property("DNS Servers", ip_config_output)
        self.data.network.gateway = self._parse_ipconfig_property("Default Gateway", ip_config_output)
        self.data.network.dhcp_server = self._parse_ipconfig_property("DHCP Server", ip_config_output)

    def run(self):
        self.get_client_net_info()
        super().run()

if __name__ == '__main__':
    local_dc = WindowsDataCollector()
    local_dc.run()
    print(local_dc.data)