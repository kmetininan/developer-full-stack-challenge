from pydantic import BaseModel
from typing import List
import datetime


# Authentication schemas
class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenPayloadSchema(BaseModel):
    username: str


class UserSchema(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserInDBSchema(UserSchema):
    password: str


# Book schema
class BookBaseSchema(BaseModel):
    title: str
    pages: int


class BookCreateSchema(BookBaseSchema):
    author_id: int


class BookEditSchema(BookBaseSchema):
    pass


class BookSchema(BookBaseSchema):
    id: int

    class Config:
        orm_mode = True


# Author schema
class AuthorBaseSchema(BaseModel):
    name: str


class AuthorCreateSchema(AuthorBaseSchema):
    pass


class AuthorSchema(AuthorBaseSchema):
    id: int
    num_books: int
    books: List[BookSchema]

    class Config:
        orm_mode = True


class AuthorsResponseSchema(BaseModel):
    authors: List[AuthorSchema]


class AuthorResponseSchema(AuthorBaseSchema):
    id: int
    num_books: int

    class Config:
        orm_mode = True


class BookResponseSchema(BookBaseSchema):
    id: int
    author_id: int
    author: AuthorResponseSchema

    class Config:
        orm_mode = True


class BooksSchema(BaseModel):
    books: List[BookResponseSchema]
