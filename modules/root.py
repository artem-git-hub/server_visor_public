from typing import Optional

from fastapi import APIRouter, Request, Cookie
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix='', tags=['root'])

templates = Jinja2Templates(directory="templates")


@router.get('/', response_class=HTMLResponse)
def main_page(request: Request, session: Optional[str] = Cookie(default=None)):
    return templates.TemplateResponse("root.html", {"request": request})
