from ..routers.auth import get_current_user, get_db, authenticate_user, create_access_token, SECRET_KEY, ALGORITHM
from jose import jwt, JWTError
from datetime import timedelta, datetime, timezone
from .utils import *
import pytest
from fastapi import HTTPException

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_user_login(test_user):
    db = TestingSessionLocal()
    authenticated_user = authenticate_user(test_user.username, "testpassword", db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username
    assert authenticated_user.id == test_user.id

    non_existent_user = authenticate_user("wronguser", "testpassword", db)
    assert non_existent_user is False

    wrong_password_user = authenticate_user(test_user.username, "wrongpassword", db)
    assert wrong_password_user is False

def test_create_access_token(test_user):
    expired_delta = timedelta(days=1)
    token  = create_access_token(test_user.username, test_user.id, test_user.role, expired_delta)
    decode_token = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM, options={"verify_exp": False})
    assert decode_token.get('sub') == test_user.username
    assert decode_token.get('id') == test_user.id
    assert decode_token.get('role') == test_user.role



@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {'sub': 'testuser' , 'id': 1, 'role': 'ADMIN'}
    token = jwt.encode(encode, SECRET_KEY, algorithm =ALGORITHM)
    current_user = await get_current_user(token)
    assert current_user == {'username': 'testuser', 'id': 1, 'role': 'ADMIN'}


@pytest.mark.asyncio
async def test_get_current_user_missinng_payload():
    encode = {'role': 'USER'}
    token = jwt.encode(encode, SECRET_KEY, algorithm =ALGORITHM)
    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token)
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Could not verify the user"