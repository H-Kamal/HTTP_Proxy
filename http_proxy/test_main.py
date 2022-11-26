import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .database import Base
from .main import app, get_db

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


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_and_read_URL(test_db):
    response = client.post(
        "/urlset/",
        json={"url": "www.google.com", "allowed": True},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["url"] == "www.google.com"
    assert data["allowed"] == True
    url = data["url"]

    response = client.get(f"/v1/urlinfo/?resource_url_with_query_string={url}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["url"] == "www.google.com"
    assert data["allowed"] == True

# Tests that the base URL is stored and queried instead of the whole URL
def test_base_url_storage(test_db):
    response = client.post(
        "/urlset/",
        json={"url": "https://www.cbc.ca/news/canada/british-columbia", "allowed": True},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["url"] == "www.cbc.ca"
    assert data["allowed"] == True
    url = "https://www.cbc.ca/news/canada/british-columbia"

    response = client.get(f"/v1/urlinfo/?resource_url_with_query_string={url}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["url"] == "www.cbc.ca"
    assert data["allowed"] == True

# Posts an invalid URL and receives error 400 
def test_broken_url_post(test_db):
    response = client.post(
        "/urlset/",
        json={"url": "https://www.c!bc.ca/news/canada/british-columbia", "allowed": True},
    )
    assert response.status_code == 400, response.text

# GET a URL that doesn't exist in the DB
def test_missing_query_url(test_db):
    response = client.get(f"/v1/urlinfo/?resource_url_with_query_string=www.missing.com")
    assert response.status_code == 404, response.text

# Tests variations of URLs
def test_base_url_storage(test_db):
    urlList = ["www.abc.ca/news/canada/british-columbia", "www.bbc.ca/",
                "www.cbc.ca/?q=hello"]

    for idx, url in enumerate(urlList):
        response = client.post(
            "/urlset/",
            json={"url": url, "allowed": True},
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["url"] == "www." + chr(ord('a') + idx)  + "bc.ca"
        assert data["allowed"] == True
        url = data["url"]

        response = client.get(f"/v1/urlinfo/?resource_url_with_query_string={url}")
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["url"] == "www." + chr(ord('a') + idx)  + "bc.ca"
        assert data["allowed"] == True
