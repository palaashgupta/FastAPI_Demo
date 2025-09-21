
from ..main import app
from ..routers.admin import get_current_user, get_db
from fastapi import status
from ..models import Todos
from .utils import *


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_admin_read_all_authenticated(test_todo):
    response = client.get("/admin/todo")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'complete':False, 'title': 'Test Todo', 'description': 'This is a test todo', 'id': 1, 'priority': 1, 'owner_id': 1}
    ]

def test_admin_delete_todo(test_todo):
    response = client.delete("/admin/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    todo = db.query(Todos).filter(Todos.id == 1).first()
    assert todo is None

def test_admin_delete_todo_not_found():
    response = client.delete("/admin/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": 'Todo item with the id 999 is not found'}