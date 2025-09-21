from fastapi import APIRouter,Depends,HTTPException,status, Path
from ..models import Todos
from ..database import  SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from .auth import get_current_user




router = APIRouter()
 



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class TodoRequest(BaseModel):
    title: str = Field(min_length = 3)
    description: str = Field(min_length = 3, max_length=100)
    priority: int = Field(gt = 0 ,lt = 6)
    complete: bool
    

### Read

@router.get("/")
async def read_all(user: user_dependency,db:db_dependency, status_code= status.HTTP_200_OK):
    
    if user is None:
        raise HTTPException(status_code= 401, detail ='Could not verify the user')
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()



@router.get("/todo/{todo_id}",status_code= status.HTTP_200_OK)
async def read_by_id(users: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if users is None:
        raise HTTPException(status_code= 401, detail ='Could not verify the user')
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == users.get('id')).first()
    
    if todo_model is not None:
        return todo_model
    
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "ID not found in the Database.")


### CREATE NEW RECORD

@router.post("/todo", status_code= status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest):

    if user is None:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail ='Could not verify the user')
    
    
    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get('id'))

    db.add(todo_model)
    db.commit()


### UPDATE A RECORD

@router.put("/todo/{update_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_id(user: user_dependency, 
                    db:db_dependency,
                    todo_request: TodoRequest,
                    update_id: int = Path(gt = 0)):
    if user is None:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail ='Could not verify the user')
    
    todo_model = db.query(Todos).filter(Todos.id == update_id).filter(Todos.owner_id == user.get('id')).first()

    if todo_model is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail ="ID not found in the Database.")
    
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()

### DELETE

@router.delete("/todo/{todo_id}",status_code= status.HTTP_204_NO_CONTENT)
async def delete_id(user: user_dependency,
                db:db_dependency,
                todo_id: int = Path(gt = 0)
                    ):
    if user is None:
        raise HTTPException(status_code= 401, detail ='Could not verify the user')
    
    todo_model= db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="ID not found in the Database.")
    
    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).delete()
    db.commit()