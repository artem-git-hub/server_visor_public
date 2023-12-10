import logging

import subprocess
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)

def get_process_uptime(service_name: str) -> timedelta:
    """Return uptime process in type = timedelta"""
    start_time_cmd = f"systemctl show {service_name}.service --property=ActiveEnterTimestamp --value"
    start_time = subprocess.check_output(start_time_cmd, shell=True, text=True).strip()
    if start_time is not None:
        current_time = datetime.now()
        parsed_date = datetime.strptime(start_time, "%a %Y-%m-%d %H:%M:%S %Z")
        time_difference = current_time - parsed_date
        uptime_str = f"{str(time_difference.days).rjust(2, '0')} days | {str(time_difference.seconds // 3600).rjust(2, '0')}:{str((time_difference.seconds // 60) % 60).rjust(2, '0')}:{str(time_difference.seconds % 60).rjust(2, '0')}"
        return uptime_str
    else:
        return start_time


def get_process_pid(service_name: str) -> int:
    """Return PID by name process"""
    pid_cmd = f"systemctl show {service_name}.service --property=MainPID --value"
    pid = int(subprocess.check_output(pid_cmd, shell=True, text=True).strip())
    return pid


def get_process_is_failed(service_name: str) -> int:
    """Return is_failed process"""
    result = subprocess.run(["systemctl", "is-failed", f"{service_name}.service"], capture_output=True, text=True)
    service_status = result.stdout.strip()
    return service_status.replace(" ", "")

def get_journal_logs(service_name: str) -> str:
    """Return last 100 lines logs process by name"""

    # logs_cmd = f"journalctl -u {service_name}.service | tail -n 50"
    logs_cmd = f"journalctl -u {service_name}.service --lines 70"
    logs = subprocess.check_output(logs_cmd, shell=True, text=True).strip()
    return logs

def restart_process(service_name: str):
    """command restart-or-reload of process"""

    command = f"systemctl reload-or-restart {service_name}.service"
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        logger.error("Error in block: restart process (services/systemd/sys_operation)\nmsg: {e}")



def stop_process(service_name: str):
    """STOP of process"""

    command = f"systemctl stop {service_name}.service"
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        logger.error("Error in block: stop process (services/systemd/sys_operation)\nmsg: {e}")


def create_and_start_process(service_name: str, service_file: str):
    """Make .service file and running process"""

    try:

        # Создание файла службы
        with open(f"/etc/systemd/system/{service_name}.service", 'w', encoding="utf-8") as file:
            file.write(service_file)

        # Запуск остальных команд
        commands = [
            f'systemctl enable {service_name}.service',
            'systemctl daemon-reload',
            f'systemctl start {service_name}.service'
        ]

        for cmd in commands:
            subprocess.run(cmd, shell=True, check=True)
        return "success"

    except subprocess.CalledProcessError as e:
        logger.error("Error in block: create process (services/systemd/sys_operation)\nmsg: {e}")
        return e


def delete_process(service_name: str):
    """stop process and delete .service file"""

    try:

        # Запуск остальных команд
        commands = [
            f'systemctl stop {service_name}.service',
            f'systemctl disable {service_name}.service',
            f'rm -rf /etc/systemd/system/{service_name}.service',
            f'rm -rf /etc/systemd/system/multi-user.target.wants/{service_name}.service',
            f'systemctl daemon-reload',
        ]

        for cmd in commands:
            subprocess.run(cmd, shell=True, check=True)
        return "success"

    except subprocess.CalledProcessError as e:
        logger.error("Error in block: create process (services/systemd/sys_operation)\nmsg: {e}")
        return e


