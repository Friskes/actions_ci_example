"""
Модуль для теста ответа эндпоинтов
"""

from fastapi.testclient import TestClient

from src.app import app
from src.settings import settings


# echo "START PYTEST"; pytest ./tests; echo "START MYPY"; mypy ./src ./tests; echo "START PYLINT"; pylint ./src ./tests
def test_answer():
    """
    Тест главного эндпоинта
    """
    client = TestClient(app)
    result = client.get(settings.main_url)
    assert result.status_code == 200
    assert result.json() == {
        "status": "ok",
        "message": "CI/CD works perfectly!"
    }
