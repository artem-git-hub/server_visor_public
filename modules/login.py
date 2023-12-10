import json

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates

from misc.cookie_operation import sign_data
from misc.password_operation import verifide_admin_password


router = APIRouter(prefix='/login', tags=['login'])

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request,})



@router.post("/")
def login_access(request: Request, username: str = Form(...), password : str = Form(...)) -> Response:

    # print(request)
    if username=='admin' and verifide_admin_password(password=password):
        
        user_ip = request.client.host
        signed_session = sign_data(user_ip)
        # response = RedirectResponse(request.base_url)
        # response.set_cookie(key="session", value=signed_session)
        # return response
    
        response_json = json.dumps(
            {
                "success": True,
                "message" : "Ок!"
            }
        )
        response = Response(response_json, media_type="application/json")
        response.set_cookie(key="session", value=signed_session, path="/admin")
        return response
    else:
        response_json = json.dumps(
            {
                "success": False,
                "message" : "Ты хто!????"
            }
        )
        return Response(response_json, media_type="application/json")
    
