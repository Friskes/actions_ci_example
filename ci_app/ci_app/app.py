# coding=utf-8

"""
Главный модуль для сервера деплоя
"""

import os
import sys
import logging
from typing import Annotated

import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from ci_app.logger import init_logging
from ci_app._docker import (
    get_active_containers,
    get_container_name,
    deploy_new_container
)


log = logging.getLogger(__name__)

app = FastAPI()

# Берем наш токен из переменной окружения
DEPLOYMENT_TOKEN = os.getenv('DEPLOYMENT_TOKEN', None)


class Payload(BaseModel):
    """
    Модель для эндпоинта деплоя нового контейнера
    """
    owner: str
    repository: str
    tag: str
    ports: dict[str, int] | None = None


def verify_token(Authorization: Annotated[str, Header()]):
    """
    Проверка Authorization токена на валидность
    """
    if Authorization != DEPLOYMENT_TOKEN:
        raise HTTPException(status_code=401, detail="Bad token")


@app.get('/', dependencies=[Depends(verify_token)])
def get_all_active_containers():
    """
    Получение списка всех активных контейнеров,
    возвращает json со всеми активными контейнерами на хосте.
    """
    return jsonable_encoder(get_active_containers())


@app.post('/', dependencies=[Depends(verify_token)])
def create_new_container(data: Payload):
    """
    Деплой нового контейнера.\n
    Пример тела запроса:
    >>> {
            "owner": "friskes",
            "repository": "actions_ci_example",
            "tag": "v0.0.1",
            "ports": {"8080": 8080}
        }
    """
    data_dump = data.model_dump()
    log.info(f'Recieved {data_dump}')
    image_name, container_name = get_container_name(data_dump)
    result, status = deploy_new_container(image_name, container_name, data.ports)
    return JSONResponse(jsonable_encoder(result), status)


def main():
    """
    Точка входа для сервера деплоя
    """
    init_logging()
    if not DEPLOYMENT_TOKEN:
        log.error('There is no auth token in env')
        sys.exit(1)
    uvicorn.run(app, host="0.0.0.0", port=5000)


if __name__ == '__main__':
    main()
