from app.config.db import get_database_url


def test_get_database_url_uses_environment_override(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://postgres:root@localhost:5432/grants_svc_test")

    assert get_database_url() == "postgresql+asyncpg://postgres:root@localhost:5432/grants_svc_test"
