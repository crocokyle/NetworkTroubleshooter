import subprocess
import socket

def run_command(command: list[str]) -> str:
    try:
        raw_output = subprocess.run(command, stdout=subprocess.PIPE)
        return raw_output.stdout.decode('utf-8')
    except OSError:
        raise Exception(f'Error running command: {command}')

def get_client_net_details() -> dict[str:str]:
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    ip_config_output = run_command(['ipconfig', '/all'])

    return {"hostname": hostname, "ip": ip_address}


if __name__ == '__main__':
    get_client_net_details()