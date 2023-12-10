# Server visor

## Краткое описание
Сервис предназанчен для контроля за systemd сервисами работающими на текущем устройстве. Работает на fetch запросах к Backend-у, получает ответ и формирует HTML страницу. На стороне Backend-a просиходит исполнение команд и получение ответа от выполнения этих команд, этот ответ отправляется обратно. Сделано как монолитное приложение, для отображения обычные template в FastAPI.

## Использованные технологии

**Back часть:**  
- Python 3.10
- FastAPI
- SQLAlchemy
- uvicorn
- SQLite

**Front часть:**  
- JavaScript
- HTML
- CSS

## Запуск
1) установите python и клонируйте репозиторий
2) Запишите соль для cookie и пароля в .env файл  
a. Соли создаются командой bash: `openssl rand -hex 32`
b. Запишите соли в .env:  
```env
COOKIE_SALT=aeae6cd09984f5c19b9bfd9f61cf7e7354c6d34e3dce225d35f6315a300e1c57

PASSWORD_SALT=8db566535920f892d8888b1093360b1cf9de19bb2a6c1424831265fc2d5b4f9d
```
c. Захешируйте пароль для пользователя следующим кодом на Python (можно выполнить прям в терминале):  
```python
import hashlib

hashlib.sha256(("password123" + PASSWORD_SALT).encode()).hexdigest()

"password123" - замените на ваш пароль
```
3) Создайте и запустите виртуальное окружение:
```bash
python -m venv venv
source ./venv/bin/activate
```

4) Установите зависимости в виртуальное окружение:
```bash
pip install -r requirements.txt
```

5) Запустите проект:
```shell
uvicorn server:app --reload --port 8000
```

6) Перейдите по ссылке: http://localhost:8000/admin