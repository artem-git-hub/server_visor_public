import atexit
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from modules.admin import router as admin_router
from modules.login import router as login_router
from modules.process import router as process_router
from modules.root import router as root_router
from services.db.db import on_shutdown, on_startapp

app  = FastAPI()


def main():
    startapp()
    atexit.register(shutdown)


def startapp():
    #startapp fastapi
    app.mount("/static", StaticFiles(directory="static"), name="static")

    #included diferent routers from modules
    app.include_router(admin_router)
    app.include_router(login_router)
    app.include_router(process_router)
    app.include_router(root_router)

    #startapp sqlite
    on_startapp()
    print("\n\n----------------\n\nstart application\n\n----------------\n\n")


def shutdown():
    #shutdown sqlite
    on_shutdown()
    print("\n\n----------------\n\nstop application\n\n----------------\n\n")

if __name__ == "server":
    main()
