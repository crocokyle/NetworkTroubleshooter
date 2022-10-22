import re
from utils.operating_system import legacy_run_command

class Endpoint:
    def __init__(self, name, ip):
        self.name = name
        self.ip = ip
        self.status = "offline"
        self.packet_loss = 100

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

        return self.status, self.packet_loss


if __name__ == '__main__':
    router = Endpoint("Router", "192.168.86.1")
    print(router.test())