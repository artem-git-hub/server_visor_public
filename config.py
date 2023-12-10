from dataclasses import dataclass
from environs import Env
from sqlalchemy.orm import Session


@dataclass
class AdminData:
    username: str
    password: str


@dataclass
class SaltData:
    cookie_salt: str
    password_salt: str


@dataclass
class DbData:
    debug: bool
    session: Session = None





@dataclass
class Config:
    admin: AdminData
    salts: SaltData
    db: DbData


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    config = Config(
        admin=AdminData(
            username=env.str('ADMIN_USERNAME'),
            password=env.str('ADMIN_PASS'),
        ),
        salts=SaltData(
            cookie_salt=env.str('COOKIE_SALT'),
            password_salt=env.str('PASSWORD_SALT'),
        ),
        db=DbData(
            debug=env.bool("DB_DEBUG")
        ),
    )
    return config

config = load_config("./.env")