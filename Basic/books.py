from fastapi import FastAPI, Body
from Data_books import BOOKS

app = FastAPI()



### Search OR Retrieve

@app.get("/books") 
async def read_all_books(): 
    return BOOKS



@app.get("/books/{book_title}")
def read_all_titles_by_query(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return {
                "Author":book.get('author'),
                "Category":book.get('category')
            }
        
@app.get("/books/Category/ ")
def read_all_category_by_query(book_category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == book_category.casefold():
            books_to_return.append(book)
    return books_to_return

@app.get("/books/Author/ ")
def read_all_author_by_query(author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            books_to_return.append(book)
    return books_to_return
        
@app.get("/books/{book_author}/")
def read_all_Author_and_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

#### Add NEW Data

@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)

### UPDATE DATA

@app.put("/books/update_book")
async def update_book(update_book = Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == update_book.get('title').casefold():
            BOOKS[i] = update_book

### Delete Data

@app.delete("/books/delete_book/{book_title}")
async def felete_book(book_title:str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break
