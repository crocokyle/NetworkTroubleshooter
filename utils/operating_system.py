import subprocess
import time
from PyQt5.QtCore import QProcess


def _get_completed_stdout(process: QProcess) -> str:
    return process.readAllStandardOutput().data().decode()

def legacy_run_command(command: list[str])-> str:
    print(f"Running {' '.join(command)}...")
    try:
        raw_output = subprocess.run(command, stdout=subprocess.PIPE)
        return raw_output.stdout.decode('utf-8')
    except OSError:
        raise Exception(f'Error running command: {command}')

def run_command(command: list[str], console_process: QProcess) -> str:
    try:
        console_process.setProgram(command[0])
        if len(command) > 1:
            console_process.setArguments(command[1:])
        while not console_process.finished:
            time.sleep(1)
        raw_output = console_process.readAllStandardOutput().data().decode()
        return raw_output
    except Exception as e:
        raise Exception(f'Error running command: {command}\n {e}')



if __name__ == '__main__':
    print(legacy_run_command(['ping', 'google.com']))