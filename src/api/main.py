from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

from fastapi_login.exceptions import InvalidCredentialsException
from fastapi_login import LoginManager

from typing import Optional
import models
import crud

from database import engine, DBContext, get_db
from sqlalchemy.orm import Session

from schema import Book, BookRead, AuthorRead, AuthorCreate

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET = "super-secret-key"
manager = LoginManager(SECRET, '/login')

@manager.user_loader()
def get_user(email: str, db: Session = None) -> Optional[models.User]:
    """ Return the user with the corresponding email """
    if db is None:
        # No db session was provided so we have to manually create a new one
        # Closing of the connection is handled inside of DBContext.__exit__
        with DBContext() as db:
            return db.query(models.User).filter(models.User.username == email).first()
    else:
        return db.query(models).filter(models.User.username == email).first()


@app.post('/login')
def login(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    user = get_user(email)
    if not user:
        # Raise same error to ensure that no information
        # can be extracted from a failure request
        # ie if user has an account on the platform
        raise InvalidCredentialsException
    elif password != user.password:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data={'sub': email}
    )
    return {'name': user.name,'access_token': access_token}


@app.get("/authors", response_model=list[AuthorRead])
def read_authors(skip: int = 0, limit: int = 100, q: str = "", db: Session = Depends(get_db), _=Depends(manager)):
    authors = crud.get_authors(q, db, skip=skip, limit=limit)
    return authors

@app.post("/authors", response_model=AuthorCreate)
def create_author(author: AuthorCreate, db: Session = Depends(get_db), _=Depends(manager)):
    return crud.create_author(db, author=author)

@app.put("/authors/{author_id}", response_model=AuthorCreate)
def update_author(author_id: int, author: AuthorCreate, db: Session = Depends(get_db), _=Depends(manager)):
    return crud.update_author(db, author_id, author)

@app.delete("/authors/{author_id}")
def delete_author(author_id: int, db: Session = Depends(get_db), _=Depends(manager)):
    return crud.delete_author(db, author_id)

@app.get("/books", response_model=list[BookRead])
def read_books(skip: int = 0, limit: int = 100, q: str = "", db: Session = Depends(get_db), _=Depends(manager)):
    books = crud.get_books(q, db, skip=skip, limit=limit)
    return books

@app.post("/books")
def create_book(book: Book, db: Session = Depends(get_db), _=Depends(manager)):
    return crud.create_book(db=db, book=book)

@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book: Book, db: Session = Depends(get_db), _=Depends(manager)):
    return crud.update_book(db, book_id, book=book)

@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db), _=Depends(manager)):
    return crud.delete_book(db, book_id)
