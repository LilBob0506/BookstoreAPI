from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange


app = FastAPI()

class Book(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


books = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, 
        {"title": "favorite foods", "content": "I like pizza", "id" : 2}]

def find_book(id):
    for p in books:
        if p["id"] == id:
            return p

def find_index_book(id):
    for i, p in enumerate(books):
        if p['id'] == id:
            return i

@app.get("/")
def root():
    return {"message": "welcome to my api"}

@app.get("/books")
def get_books():
    return {"data": books}

@app.post("/books", status_code=status.HTTP_201_CREATED)
def add_books(book: Book):
    book_dict = book.model_dump()
    book_dict['id'] = randrange(0, 10000000)
    books.append(book_dict)
    return {"data": book_dict}

@app.get("/books/{id}")
def get_book(id: int):

    book = find_book(id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"book with id: {id} was not found")
    return {"book_detail": book}

@app.delete("/books/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(id: int):
    index = find_index_book(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"book with id: {id} does not exist")

    books.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/books/{id}")
def update_book(id: int, book: Book):
    index = find_index_book(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"book with id: {id} does not exist")

    book_dict = book.model_dump()
    book_dict['id'] = id
    books[index] = book_dict
    return {"book_dict": book_dict}