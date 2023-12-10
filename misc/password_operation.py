import hashlib

from config import config

def verifide_admin_password(password: str) -> bool:
    """Проверяет правильность введенного пароля администратора"""

    password_hash = hashlib.sha256((password + config.salts.password_salt).encode()).hexdigest()
    return password_hash == config.admin.password