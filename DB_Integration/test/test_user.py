from ..main import app
from ..routers.user import get_current_user, get_db
from fastapi import status
from ..models import Users
from .utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == test_user.username
    assert response.json()['id'] == test_user.id
    assert response.json()['role'] == test_user.role
    assert response.json()['email'] == test_user.email
    assert response.json()['first_name'] == test_user.first_name
    assert response.json()['last_name'] == test_user.last_name
    assert response.json()['phone_number'] == test_user.phone_number
    
def test_change_password(test_user):
    response = client.put("/user/password", json={"password": "testpassword", "new_password": "newtestpassword"})
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_change_password_incorrect_old_password(test_user):
    response = client.put("/user/password", json={"password": "wrongpassword", "new_password": "newtestpassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == "Wrong Password"

def test_change_phone_number(test_user):
    response = client.put("/user/phone_number/1234567890")
    assert response.status_code == status.HTTP_204_NO_CONTENT
