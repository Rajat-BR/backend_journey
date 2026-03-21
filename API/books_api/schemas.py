from pydantic import BaseModel

class Book(BaseModel):
    title: str
    author: str
    is_read: bool = False

class BookOut(BaseModel):
    id: int
    title: str
    author: str
    is_read: bool
    