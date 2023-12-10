import json
import logging
from typing import List

from fastapi import APIRouter, Form, Request, Body
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates

from services.db.iteraction.process import add_process, select_all_processes
from services.db.iteraction.process import delete_process as db_delete_process
from services.systemd.sys_operation import get_journal_logs,\
    get_process_is_failed, get_process_pid, get_process_uptime, \
    restart_process, stop_process, create_and_start_process
from services.systemd.model import SystemdProcess
from services.systemd.sys_operation import delete_process as systemd_delete_process

router = APIRouter(prefix='/process', tags=['process'])

templates = Jinja2Templates(directory="templates")

logger = logging.getLogger(__name__)


@router.post("/refresh/{name}", response_class=HTMLResponse)
def refresh(request: Request, name: str, data: dict = Body(...)):
    """Return updated json data for process [is_failds, uptime, pid, logs]"""

    with_logs = data["with_logs"]

    logs = get_journal_logs(name) if with_logs else "Logs loading ..."


    answer_dict = {
        "is_failed": get_process_is_failed(name),
        "uptime": get_process_uptime(name),
        "pid": get_process_pid(name),
        "logs": logs, 
    }

    response_json = json.dumps(answer_dict)

    response = Response(response_json, media_type="application/json")
    return response

@router.get("/restart/{name}", response_class=HTMLResponse)
def restart(request: Request, name: str):
    """Restart process"""

    dict_of_answer = {}
    try:
        restart_process(service_name=name)


        dict_of_answer = {
            "success": True,
            "error_msg": None,
        }
    except Exception as e:
        dict_of_answer = {
            "success": False,
            "error_msg": e,
        }
    finally:
        response_json = json.dumps(dict_of_answer)
        response = Response(response_json, media_type="application/json")
        return response
    

@router.get("/stop/{name}", response_class=HTMLResponse)
def stop(request: Request, name: str):
    """stoping process"""

    dict_of_answer = {}
    try:
        stop_process(service_name=name)


        dict_of_answer = {
            "success": True,
            "error_msg": None,
        }
    except Exception as e:
        dict_of_answer = {
            "success": False,
            "error_msg": e,
        }
    finally:
        response_json = json.dumps(dict_of_answer)
        response = Response(response_json, media_type="application/json")
        return response
    

@router.get('/add', response_class=HTMLResponse)
def add(request: Request):
    return templates.TemplateResponse("add_process.html", {"request": request,})


@router.get('/delete', response_class=HTMLResponse)
def delete(request: Request):
    processes = select_all_processes()

    sys_processes = []
    for process in processes:
        sysprocess = SystemdProcess(process=process)
        sys_processes.append(sysprocess)
    return templates.TemplateResponse("delete_process.html", {"request": request, "processes": sys_processes})


@router.post('/create', response_class=HTMLResponse)
def create(request: Request, data: dict = Body(...)):
    process_name = data['process_name']
    process_group = data['process_group']
    content_service = data['content_service']

    dict_of_answer = {}


    try:
        add_process(process_name, process_group)
        if content_service is not None:
            create_and_start_process(process_name, content_service)
            # systemd_delete_process(process_name)
            # db_delete_process(process_name)

        dict_of_answer = {
            "success": True,
            "error_msg": None,
        }

    except Exception as error_msg:
        dict_of_answer = {
            "success": False,
            "error_msg": error_msg,
        }
        print("\n\n------------------------\n\n\n\n", error_msg, "\n\n------------------------\n\n\n\n")
    finally:
        response_json = json.dumps(dict_of_answer)
        response = Response(response_json, media_type="application/json")
        return response
        


@router.post('/delete', response_class=HTMLResponse)
def delete_processes(request: Request, data: List[dict] = Body(...)):

    dict_of_answer = {}

    for item in data:
        answer_about_process = {}

        process_name = item["name"] 

        del_from_db = item["db"] 
        del_from_systemd = item["systemd"] 

        try:
            if del_from_db:
                db_delete_process(process_name)
            if del_from_systemd:
                systemd_delete_process(process_name)
        except Exception as error_msg:
            answer_about_process = {
                "success": False,
                "error_msg": error_msg,
            }
            logger.info("Error in delete_processes (modules/process.py)")
        finally:
            dict_of_answer[process_name] = answer_about_process

    response_json = json.dumps(dict_of_answer)
    response = Response(response_json, media_type="application/json")
    return response