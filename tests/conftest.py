
import os

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from database import Base, get_db

load_dotenv()

main_database_url = os.getenv("DATABASE_URL")

if not main_database_url:
    raise RuntimeError("DATABASE_URL is missing")

# Derive a separate test database URL.
# Never allow tests to target the main database.
from sqlalchemy.engine import make_url

main_url = make_url(main_database_url)

if main_url.database != "opspilot":
    raise RuntimeError(
        "Expected the main database to be named opspilot"
    )

test_url = main_url.set(database="opspilot_test")

if test_url.database != "opspilot_test":
    raise RuntimeError("Unsafe test database configuration")

test_engine = create_engine(
    test_url,
    poolclass=NullPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


@pytest.fixture
def client():
    # Import models so all tables are registered.
    import models
    from main import app

    # Rebuild only the dedicated test database.
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=test_engine)

