from ..db.iteraction.process import select_process
from ..db.models.process import Process
from .sys_operation import get_process_is_failed, get_journal_logs, get_process_pid, get_process_uptime

import time

class SystemdProcess():
    """class systemd process with all params for sending to frontend"""

    name: str
    group: str
    pid: int
    is_failed: str
    uptime: str
    logs: str

    process: Process


    def __init__(self, process: Process = None, without_logs: bool = True) -> None:
        """may pass all params [str and int] or pass only Process param - this is will been working"""
        
        start_init_time = time.time()

        self.process = process
        
        db_process = select_process(name=process.name)
        self.name = process.name
        self.group = db_process.group
        db_time = time.time()


        pid = get_process_pid(process.name)
        self.pid = pid
        pid_time = time.time()


        is_failed = get_process_is_failed(process.name)
        self.is_failed = is_failed
        is_failed_time = time.time()


        uptime_str = get_process_uptime(process.name)
        self.uptime = uptime_str
        uptime_time = time.time()
        
        if without_logs:
            logs = "Logs loading ..."
        else:
            logs = get_journal_logs(service_name=process.name)
        self.logs = logs
        logs_time = time.time()
        
        
        print(f"------ db_time: {db_time - start_init_time}")
        print(f"------ pid_time: {pid_time - db_time}")
        print(f"------ is_failed_time: {is_failed_time - pid_time}")
        print(f"------ uptime_time: {uptime_time - is_failed_time}")
        print(f"------ logs_time: {logs_time - uptime_time}")
        print(f"------ all_time: {logs_time - start_init_time}")


        return




    def get_process(self):
        """Returned full filled SystemdProcess"""

        process_name = self.process.name

        pid = get_process_pid(process_name)
        self.pid = pid

        is_failed = get_process_is_failed(process_name).replace(" ", "")
        self.is_failed = is_failed


        uptime_timedelta = get_process_uptime(process_name)
        uptime_str = f"{uptime_timedelta.days} days | {uptime_timedelta.seconds // 3600}:{(uptime_timedelta.seconds // 60) % 60}:{uptime_timedelta.seconds % 60}"
        self.uptime = uptime_str
        
        logs = get_journal_logs(service_name=process_name)
        self.logs = logs


        return self


