# Local imports
from utils.operating_system import legacy_run_command
from utils.network import Endpoint, is_same_24_subnet
from data_collectors.abstract import DataCollector

# 3rd party imports
import re
from netaddr import IPAddress, AddrFormatError
from PyQt5.QtCore import QProcess


# TODO: Specify Windows/linux - maybe use remote rather than discovery
class DicoveryDataCollector(DataCollector):
    def __init__(self):
        super().__init__()

    @staticmethod
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

    # TODO: cleanup unused params
    def get_private_ips(self, console_process: QProcess) -> list[IPAddress]:
        tracert_output = legacy_run_command(['tracert', '8.8.8.8'])
        hops = self._parse_tracert(tracert_output)
        internal_ips = []
        for hop in hops:
            if hop.is_private():
                internal_ips.append(hop)

        return internal_ips

    # TODO: cleanup unused params
    def get_internal_endpoints(self, console_process: QProcess) -> list[Endpoint]:
        private_ips: list[IPAddress] = self.get_private_ips(console_process)
        # TODO: DO SOMETHING client_info:dict[str:str] = get_client_net_info()
    
    def run(self):
        # TODO: implement
        super().run()
    
def get_localhost_ip() -> str:
    pass

if __name__ == '__main__':
    print(get_internal_endpoints("TODO"))
