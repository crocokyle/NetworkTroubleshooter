# Local imports
from utils.operating_system import legacy_run_command

#3rd party imports
import re
from datetime import datetime
from netaddr import IPAddress
from typing import Union

class Endpoint:
    def __init__(self, name, ip):
        self.name = name
        self.ip = ip
        self.status = "offline"
        self.packet_loss = 100
        self.last_run = datetime.fromtimestamp(0)

    def __str__(self) -> str:
        return f"Name: {self.name}\nIP: {self.ip}\nStatus: {self.status}\nPacket Loss: {self.packet_loss}\nLast Test: {self.last_run}"

    def append(val) -> None:
        super().run()
        # TODO: implement isinstance for Endpoint vs IP???
        
    def test(self):
        ping_result = legacy_run_command(['ping', self.ip]).splitlines()[8].strip()
        if match := re.search(r'\((\d+)% loss\)', ping_result):
            self.packet_loss = int(match.group(1))
            if self.packet_loss == 0:
                self.status = "online"
            elif self.packet_loss == 100:
                self.status = "offline"
            else:
                self.status = "intermittent"
        else:
            self.status = "Error parsing ping results!"

        self.last_run = datetime.now()
        return self.status, self.packet_loss


def is_same_24_subnet(ip1: Union[IPAddress,str], ip2: Union[IPAddress,str]) -> bool:
    if isinstance(ip1, str):
        ip1 = IPAddress(ip1)
    if isinstance(ip2, str):
        ip2 = IPAddress(ip2)

    return ip1.words[0:3] == ip2.words[0:3]

if __name__ == '__main__':
    router = Endpoint("Router", "192.168.86.1")
    my_pc = Endpoint("my_pc", "192.168.86.123")
    print(is_same_24_subnet(router.ip, my_pc.ip))
    print(is_same_24_subnet("192.168.1.1", "10.1.1.123"))