from pydantic import BaseModel, Field, validator

from typing import Optional

class AuthorForBook(BaseModel):
    id: int
    name: str = Field(min_length=1)
    
    class Config:
        orm_mode = True

class AuthorBase(BaseModel):
    name: str = Field(min_length=1)
    
    class Config:
        orm_mode = True

class AuthorCreate(AuthorBase):
    books: object = Field()
    pass

class AuthorRead(AuthorBase):
    id: int
    books: object = Field()
    # books: object = Field(exclude=True) // to split into two endpoints
    count_of_books: Optional[int]

    @validator('count_of_books', pre=True, always=True)
    def make_count_of_books(cls, v: str, values: dict):
        return len(values['books'])

    class Config:
        orm_mode = True

class BookBase(BaseModel):
    name: str
    pages_count: int

class BookCreate(BookBase):
    pass

class Book(BookBase):
    author_id: int

    class Config:
        orm_mode = True

class BookRead(BookBase):
    id: int
    author: AuthorForBook

    class Config:
        orm_mode = True