import base64
import hmac
import hashlib

from typing import Optional

from config import config

def sign_data(data: str) -> str:
    """Возвращает подписанную дату  в SHA-256
    в виде base64(data).signed_data[в SHA-256]"""

    data_b64 = base64.b64encode(data.encode()).decode()
    signed_data = get_sined_data(data)
    return f"{data_b64}.{signed_data}"

def get_sined_data(data: str) -> str:
    """Возвращает подписанную дату  в SHA-256, одно слово return=as2...5f1"""
    return hmac.new(
        config.salts.cookie_salt.encode(),
        msg=data.encode(),  
        digestmod=hashlib.sha256
    ).hexdigest()

def check_valid_signed_data(data_from_cookie: str) -> Optional[str]:
    """Очищает и возвращает дату (str), если она верно подписана
    None в противном случае"""

    cookie_data, sign_data = data_from_cookie.split(".")
    data = base64.b64decode(cookie_data.encode()).decode()

    valid_signed_data = get_sined_data(data)
    if hmac.compare_digest(sign_data, valid_signed_data):
        return data