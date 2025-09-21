from ..main import app
from ..routers.todos import get_current_user, get_db
from fastapi import status
from .utils import *


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_all_authenticated(test_todo):
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'complete':False, 'title': 'Test Todo', 'description': 'This is a test todo', 'id': 1, 'priority': 1, 'owner_id': 1}]

def test_read_1_authenticated(test_todo):
    response = client.get('/todo/1')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'complete':False, 'title': 'Test Todo', 'description': 'This is a test todo', 'id': 1, 'priority': 1, 'owner_id': 1}

def test_read_one_authenticated_not_found():
    response = client.get('/todo/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'ID not found in the Database.'}

def test_create_todo(test_todo):
    request_data = {
        "title": "New Todo",
        "description": "This is a new todo",
        "priority": 2,
        "complete": False,
    }
    response = client.post('/todo/', json = request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')
  
def test_update_todo(test_todo):
    request_dat = {
        'title': 'New Todo',
        'description': 'This is a new todo',
        'priority': 2, 
        'complete': True
    }
    response = client.put('/todo/1', json = request_dat)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.complete == request_dat.get('complete')

def test_update_not_found_todo(test_todo):
    request_dat = {
        'title': 'New Todo',
        'description': 'This is a new todo',
        'priority': 2, 
        'complete': True
    }
    response = client.put('/todo/999', json = request_dat)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'ID not found in the Database.'}

def test_delete_todo(test_todo):
    response = client.delete('/todo/1')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None

def test_delete_todo_not_found(test_todo):
    response = client.delete('/todo/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'ID not found in the Database.'}