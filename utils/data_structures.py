# 3rd party imports
from enum import Enum


class Fact(Enum):
    def __init__(self, description:str, val=None):
        self.description = description
        self.val = val

# TODO: find out if facts can be structured better (use built in value)
class Data:
    class Network(Fact):
        CONNECTED_IP:str = 'connected_ip'
        CONNECTED_INTERFACE:str = 'connected_interface'
        DHCP_SERVER:str = 'dhcp_server'
        DNS_SERVER:str = 'dns_server'
        GATEWAY:str = 'gateway'
        HOSTNAME:str = 'hostname'


if __name__ == '__main__':
    my_data = Data()
    print(my_data)