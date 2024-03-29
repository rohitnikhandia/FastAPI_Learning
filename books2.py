from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()




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


class bookRequest(BaseModel):
    id: Optional[int] = Field(None, title="id is not needed")
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=250)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1999, lt=2025)


    class Config:
        json_schema_extra = {
            "example": {
                'title': 'A new book',
                'author': 'codingwithroby',
                'description': 'A new description of a book',
                'rating': 5,
                'published_date': 2000
            }
        }

def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 0
    return book

BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2012),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2021),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5, 2020),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2017),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2021),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2006)
]


@app.get("/", status_code=status.HTTP_200_OK)
async def home():
    return {"message": "Welcome to the homepage."}


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int=Path(gt=0, title="0 se bada dalna padega", description="0 se bada dal na bhai")):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(404, detail="Item not found")


@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(rating: int=Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == rating:
            books_to_return.append(book)
    return books_to_return


@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: bookRequest):
    book = book_request.model_dump()
    book_to_append = Book(**book)
    BOOKS.append(find_book_id(book_to_append))


@app.put("/book/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(update_request: bookRequest):
    flag = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == update_request.id:
            BOOKS[i] = update_request
            flag = True
    if not flag:
        raise HTTPException (404, detail="Item not found")


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int=Path(gt=0)):
    flag = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            flag = True
            break
    if not flag:
        raise HTTPException(404, detail="Item not found")


@app.get("/books/publish/", status_code=status.HTTP_200_OK)
def get_books_by_published_date(published_date: int=Query(gt=1999, lt=2025)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return
