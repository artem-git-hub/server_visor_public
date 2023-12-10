from typing import List

from sqlalchemy.orm import Session

from ..db import request
from ..models.process import Process

@request
def select_process(name: str, session: Session = None) -> Process:
    """Select process by name"""
    process = session.query(Process).where(Process.name == name).first()
    return process

@request
def select_all_processes(session: Session = None) -> List[Process]:
    processes = session.query(Process).all()
    return processes

@request
def add_process(name: str, group: str, session: Session = None) -> bool:
    """Add new process"""
    new_process = Process(name=name, group=group)
    session.add(new_process)
    session.commit()


@request
def update_process(name: str, new_name: str = None, new_group: str = None, session: Session = None) -> None:
    """Update process by name"""
    process = session.query(Process).where(Process.name == name).first()
    if new_name:
        process.name = new_name
    if new_group:
        process.name = new_name

    session.commit()

@request
def delete_process(name: str, session: Session = None) -> None:
    """Delete process by name"""
    process = session.query(Process).where(Process.name == name).first()
    session.delete(process)
    session.commit()
