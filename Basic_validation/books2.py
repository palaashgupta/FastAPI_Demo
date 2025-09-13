from fastapi import FastAPI,Body,Path, Query, HTTPException
from Data_books2 import BOOKS, BookRequest, Book
from starlette import status


app = FastAPI()

### READ BOOKS By PATH or QUERY

@app.get("/books",status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}",status_code=status.HTTP_200_OK)
async def reaad_book_by_ID(book_id: int = Path(gt = 0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail = 'Item not Found')
        

@app.get("/books/",status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0,lt=6)):
    books_to_return = []
    for book in  BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return
 

@app.get("/books/published_date/",status_code=status.HTTP_200_OK)
async def read_by_published_date(published_date: int = Query(gt = 1600, lt = 2025)):
    books_to_return = []
    for books in BOOKS:
        if books.published_date == published_date:
            books_to_return.append(books)
    return books_to_return

### INSERT A New BOOK

@app.post("/create-book",status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))
    
def find_book_id(book: Book):
    if len(BOOKS)>0:
        book.id = BOOKS[-1].id +1
    else:
        book.id = 1

    return book

### UPDATE a BOOK

@app.put("/books/update_book",status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed =True
    if not book_changed:
        raise HTTPException(status_code=404, detail = 'Item not Found')


### DELETE a BOOK

@app.delete("/books/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail = 'Item not Found')
