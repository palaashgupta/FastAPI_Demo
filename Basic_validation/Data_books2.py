from pydantic import BaseModel, Field
from typing import Optional

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int
    
    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description='Id is not needed on create', default = None)
    title: str = Field(min_length =3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1,max_length = 100)
    rating: int = Field(gt =0, lt = 6) 
    published_date: int = Field(gt = 1600, lt = 2025)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": " A new Book",
                "author": "New Author of the book",
                "description": "New description",
                "rating": 5,
                "published_date": 2002
            }
        }
    }


BOOKS = [
    Book(1,'Computer Science VOL1', 'Alan', 'Data Structure and Algorithm', 5, 2002),
    Book(2,'Computer Science VOL2', 'Alan F', 'Logic', 4, 2005),
    Book(3,'Computer Science VOL4', 'Author 1', 'Master Endpoint', 2, 2005),
    Book(4,'AI Law', 'Alan F', 'Law and Ethics', 1, 2002),
    Book(5,'AI Ethics', 'Author 1', 'Ethics Behind Ai', 3, 2019),
    Book(6,'Computer Science VOL5', 'Alan', 'Computational Time', 1, 2023)
]