from netaddr import IPAddress

from typing import Union

def is_same_24_subnet(ip1: Union[IPAddress,str], ip2: Union[IPAddress,str]) -> bool:
    if isinstance(ip1, str):
        ip1 = IPAddress(ip1)
    if isinstance(ip2, str):
        ip2 = IPAddress(ip2)

    return ip1.words[0:3] == ip2.words[0:3]

if __name__ == '__main__':
    print(is_same_24_subnet("192.168.1.1", "192.168.1.123"))
    print(is_same_24_subnet("192.168.1.1", "10.1.1.123"))