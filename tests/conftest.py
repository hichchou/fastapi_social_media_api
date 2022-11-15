from fastapi.testclient import TestClient
import pytest
from alembic import command

from tests.database import engine, TestingSessionLocal
from app.main import app
from app.database import get_db, Base
from app.oauth2 import create_acess_token
from app import models


@pytest.fixture
# fixture for created/deleting database after each test
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # can also use alembic command instead:
    # command.downgrade("base")
    # command.upgrade("head")
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {
        "email": "test@gmail.com",
        "password": "password123"
    }
    res = client.post("users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']

    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {
        "email": "test2@gmail.com",
        "password": "password123"
    }
    res = client.post("users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']

    return new_user


@pytest.fixture
def token(test_user):
    access_token = create_acess_token({"user_id": test_user["id"]})

    # return {"acess_token": access_token, "token_type": "bearer"}
    return access_token


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [
        {
            "title": "1st title",
            "content": "1st content",
            "owner_id": test_user['id']
        },
        {
            "title": "2nd title",
            "content": "2nd content",
            "owner_id": test_user['id']
        },
        {
            "title": "3rd title",
            "content": "3rd content",
            "owner_id": test_user['id']
        },
        {
            "title": "post of 2nd user",
            "content": "awesome content",
            "owner_id": test_user2['id']
        }
    ]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    post_list = list(post_map)

    session.add_all(post_list)
    session.commit()
    posts = session.query(models.Post).all()

    return posts
