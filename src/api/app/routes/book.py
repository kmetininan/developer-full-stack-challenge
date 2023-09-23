from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas
from ..database_config import get_db_session
from ..models import Book, User, Author
from ..auth_helper import get_current_user

router = APIRouter(prefix="/book", tags=["Book"])


@router.post("/", response_model=schemas.BookSchema)
def create_book(
    book: schemas.BookCreateSchema,
    authenticated_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    author = db.query(Author).filter(Author.id == book.author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    new_book = Book(title=book.title, pages=book.pages, author_id=book.author_id)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@router.get("/", response_model=schemas.BooksSchema)
def get_all_books(
    authenticated_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    books = db.query(Book).all()
    return {"books": books}


@router.get("/{book_id}", response_model=schemas.BooksSchema)
def get_book(
    book_id: int,
    authenticated_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/{book_id}", response_model=schemas.BookSchema)
def edit_book(
    book_id: int,
    book: schemas.BookEditSchema,
    authenticated_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db_book.title = book.title
    db_book.pages = book.pages
    db.commit()
    db.refresh(db_book)
    return db_book


@router.delete("/{book_id}")
def delete_book(
    book_id: int,
    authenticated_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.refresh(db_book)
    db.delete(db_book)
    db.commit()
    return {"message": "Book deleted successfully"}
