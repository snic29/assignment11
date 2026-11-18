import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
import app.models
from main import app


@pytest.fixture(scope="session")
def test_engine():
    database_url = os.environ.get(
        "DATABASE_URL", "sqlite+pysqlite:///:memory:"
    )
    engine_options = {}
    if database_url.startswith("sqlite"):
        engine_options["connect_args"] = {"check_same_thread": False}
        if database_url.endswith(":memory:"):
            engine_options["poolclass"] = StaticPool

    engine = create_engine(database_url, **engine_options)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def db_session(test_engine):
    connection = test_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_db, None)
