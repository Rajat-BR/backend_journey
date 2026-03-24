from fastapi import APIRouter
from schemas import Book, BookOut
from services.book_service import get_book, get_books, create_book, update_book, remove_book

router = APIRouter()

@router.get("/")
def home():
    return {"message": "Books API running"}

@router.post("/books")
def post(book: Book):
    create_book(book)
    return {"message": "Book created Successfully"}

@router.get("/books", response_model=list[BookOut])
def fetch_books(author: str | None = None, 
                is_read: bool | None = None,
                search: str | None = None, 
                sort: str | None = None, 
                order: str | None = None,
                limit: int | None = None,
                offset: int | None = None
                ):
    books = get_books(author, is_read, search, sort, order, limit, offset)
    return books

@router.get("/books/{book_id}", response_model=BookOut)
def fetch_book(book_id: int):
    book = get_book(book_id)
    return book

@router.put("/books/{book_id}")
def put_book(book: Book, book_id: int):
    update_book(book, book_id)
    return {"message": "Book updated successfully"}

@router.delete("/books/{book_id}")
def delete_book(book_id: int):
    remove_book(book_id)
    return {"message": "Book removed successfully"}

