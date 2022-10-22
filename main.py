
from tqdm import tqdm
from pprint import pprint

from utils.network import Endpoint


def validate_config(endpoint_config:list[dict]) -> list[Endpoint]:
    return [Endpoint(k, v) for d in endpoint_config for k, v in d.items()]

def test_endpoints(endpoints: list[Endpoint]) -> list[Endpoint]:
    for endpoint in tqdm(endpoints):
        endpoint.test()

    return endpoints

if __name__ == "__main__":
    unit_test = b'\r\nPinging 8.8.8.8 with 32 bytes of data:\r\nReply from 8.8.8.8: bytes=32 time=79ms TTL=110\r\nReply from 8.8.8.8: bytes=32 time=42ms TTL=110\r\nReply from 8.8.8.8: bytes=32 time=60ms TTL=110\r\nReply from 8.8.8.8: bytes=32 time=50ms TTL=110\r\n\r\nPing statistics for 8.8.8.8:\r\n    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),\r\nApproximate round trip times in milli-seconds:\r\n    Minimum = 42ms, Maximum = 79ms, Average = 57ms\r\n'.decode('utf-8')

    endpoint_config = [
        {"internet": '8.8.8.8'},
        {"dns": 'google.com'},
        {"modem": '192.168.12.1'},
        {"router": '192.168.86.1'},
    ]

    validated_endpoints = validate_config(endpoint_config)
    tested_endpoints = test_endpoints(validated_endpoints)
    for endpoint in tested_endpoints:
        print(f"\n================== {endpoint.name} ==================")
        print(f"IP: {endpoint.ip}")
        print(f"Packet Loss: {endpoint.packet_loss}%")
        print(f"Status: {endpoint.status}")
        print("="*(38+len(endpoint.name)))
