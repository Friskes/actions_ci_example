"""
Главный модуль для сервера
"""

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

try:
    from settings import settings
except ImportError:
    from .settings import settings


app = FastAPI() # uvicorn src.app:app --reload


class Status(BaseModel):
    """
    Модель для главного эндпоинта
    """
    status: str = "ok"
    message: str = "CI/CD works perfectly!"


@app.get(settings.main_url)
async def status():
    """
    Главный эндпоинт
    """
    return Status()


def main():
    """
    Точка входа в приложение
    """
    uvicorn.run(app, host="0.0.0.0", port=8080)


if __name__ == '__main__':
    main()
