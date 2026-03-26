from pydantic import BaseModel, Field

class Book(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    author: str = Field(min_length=1, max_length=100)
    is_read: bool = False

class BookOut(BaseModel):
    id: int
    title: str = Field(min_length=1, max_length=100)
    author: str = Field(min_length=1, max_length=100)
    is_read: bool
    