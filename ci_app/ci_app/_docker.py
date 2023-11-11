"""
Модуль для логики докера
"""

import logging
from typing import Any

import docker


docker_client = docker.from_env()

log = logging.getLogger(__name__)


def get_active_containers() -> list[dict[str, Any]]:
    """
    Получение списка запущенных контейнеров
    """
    containers = docker_client.containers.list()
    result = []
    for container in containers:
        result.append({
            'short_id': container.short_id,
            'container_name': container.name,
            'image_name': container.image.tags,
            'created':  container.attrs['Created'],
            'status':  container.status,
            'ports':  container.ports
        })
    return result


def get_container_name(item: dict[str, str]) -> tuple[str, str]:
    """
    Получение имени image из POST запроса
    """
    if not isinstance(item, dict):
        return ''
    owner = item.get('owner')
    repository = item.get('repository')
    tag = item.get('tag', 'latest').replace('v', '')
    if owner and repository and tag:
        return f'{owner}/{repository}:{tag}', repository
    if repository and tag:
        return f'{repository}:{tag}', repository
    return '', ''


def kill_old_container(container_name: str) -> bool:
    """
    Перед запуском нового контейнера, удаляем старый
    """
    try:
        # Получение контейнера
        container = docker_client.containers.get(container_name)
        # Остановка
        container.kill()
    except Exception as e:
        # На случай если такого контейнера небыло
        log.warning(f'Error while delete container {container_name}, {e}')
        return False
    finally:
        # Удаление остановленых контейнеров, чтобы избежать конфликта имен
        log.debug(docker_client.containers.prune())
    log.info(f'Container deleted. container_name = {container_name}')
    return True


def deploy_new_container(
    image_name: str,
    container_name: str,
    ports: dict[str, int] = None
) -> tuple[dict[str, str | bool], int]:
    """
    Деплой нового контейнера
    """
    try:
        # Пул последнего image из docker hub'a
        log.info(f'pull {image_name}, name={container_name}')
        docker_client.images.pull(image_name)
        log.debug('Success')
        kill_old_container(container_name)
        log.debug('Old killed')
        # Запуск нового контейнера
        docker_client.containers.run(
            image=image_name,
            name=container_name,
            detach=True,
            ports=ports
        )
    except Exception as e:
        log.error(f'Error while deploy container {container_name}, \n{e}')
        return {'status': False, 'error': str(e)}, 400
    log.info(f'Container deployed. container_name = {container_name}')
    return {'status': True}, 200
