from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base_class import Base
from app.main import app
from app.api.deps import get_db
from app.core.config import settings

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


TEST_HEADER = {"authorization": settings.API_KEY_0}
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# def test_create_user():
#     response = client.post(
#         "/users/",
#         json={"email": "deadpool@example.com", "password": "chimichangas4life"},
#     )
#     assert response.status_code == 200, response.text
#     data = response.json()
#     assert data["email"] == "deadpool@example.com"
#     assert "id" in data
#     user_id = data["id"]

#     response = client.get(f"/users/{user_id}")
#     assert response.status_code == 200, response.text
#     data = response.json()
#     assert data["email"] == "deadpool@example.com"
#     assert data["id"] == user_id


def test_ping():
    response = client.get("/api/v1/ping", headers=TEST_HEADER)
    assert response.status_code == 200
    assert response.json() == {"environment": "dev", "ping": "pong"}


def test_meta():
    response = client.get("/api/v1/meta")
    assert response.status_cose == 200
    assert list(response.json().keys()) == [
        "id",
        "workhours",
        "workdays",
        "province",
        "vacation",
        "date_created",
        "submitter_id",
    ]


def test_create_tags():
    data = {}  # TODO: check database scheme
    response = client.post("/api/v1/tags", data=data, headers=TEST_HEADER)
    assert response.status_code == 200
    assert response.json() == {}  # TODO: check database scheme


def test_read_tags():
    response = client.get("/api/v1/tags", headers=TEST_HEADER)
    assert response.status_code == 200
    assert response.json() == {}  # TODO: check database scheme


def test_update_tags():
    data = {}  # TODO: check database scheme
    response = client.update("/api/v1/tags", data=data, headers=TEST_HEADER)
    assert response.status_code == 200
    assert response.json() == {}  # TODO: check database scheme
