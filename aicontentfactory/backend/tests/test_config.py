import pytest
from app.core.config import settings, get_database_url


def test_settings_loads():
    assert settings.HOST == "0.0.0.0"
    assert settings.PORT == 8000


def test_database_url():
    url = get_database_url()
    assert "mysql+pymysql://" in url
    assert settings.DB_USER in url
    assert settings.DB_PASSWORD in url
    assert settings.DB_HOST in url
    assert str(settings.DB_PORT) in url
    assert settings.DB_NAME in url
