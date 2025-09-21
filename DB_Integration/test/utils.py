from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..database import Base
import pytest
from fastapi.testclient import TestClient
from ..main import app
from ..models import Todos, Users
from ..routers.auth import bcrypt_context

SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, 
                       connect_args={"check_same_thread": False},
                       poolclass=StaticPool
                       )

TestingSessionLocal = sessionmaker(autocommit=False, autoflush = False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {
 'username': 'testuser', 'id': 1, 'role': 'ADMIN'

    }
client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(title="Test Todo", description="This is a test todo", priority=1,complete = False, owner_id=1)
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as conn:
        conn.execute(text('DELETE FROM todos'))
        conn.commit()

@pytest.fixture
def test_user():
    user = Users(username="testuser", email=None, first_name=None, last_name=None, role="ADMIN", phone_number=None, hashed_password=bcrypt_context.hash("testpassword"))
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as conn:
        conn.execute(text('DELETE FROM users'))
        conn.commit()
