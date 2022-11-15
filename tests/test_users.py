from app import schemas
from app.config import settings

from jose import jwt
import pytest


def test_root(client, session):
    # session fixture allows us to have access to query the db during testing
    # e.g session.query(models.Post.id==id)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world !"}


def test_create_users(client):
    response = client.post("/users/",
                           json={"email": "test@gmail.com",
                                 "password": "password123"})
    # print(response.json())
    new_user = schemas.UserOut(**response.json())
    #assert response.json().get("email") == "test@gmail.com"
    assert new_user.email == "test@gmail.com"
    assert response.status_code == 201


def test_login_user(client, test_user):
    # print(test_user)
    response = client.post("/login",
                           data={"username": test_user["email"],
                                 "password": test_user["password"]})

    # print(response.json())
    login_res = schemas.Token(**response.json())
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert response.status_code == 200


@pytest.mark.parametrize("email, password, stat", [
    ('test@gmail.com', 'wrongPassword', 403),
    ('wrongEmail@gmail.com', 'password123', 403),
    ('wrongEmail@gmail.com', 'wrongPassword', 403),
    (None, 'password123', 422),
    ('test@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, stat):
    response = client.post("/login", data={
        "username": email,
        "password": password
    })

    assert response.status_code == stat
    #assert response.json().get('detail') == 'Invalid Credentials'
