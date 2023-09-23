from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas
from ..database_config import get_db_session
from ..models import Author, User
from ..auth_helper import get_current_user

router = APIRouter(prefix="/author", tags=["Author"])


@router.post("/", response_model=schemas.AuthorSchema)
def create_author(
    author: schemas.AuthorCreateSchema,
    authenticated_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    new_author = Author(name=author.name)
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


@router.get("/", response_model=schemas.AuthorsResponseSchema)
def get_all_authors(
    authenticated_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    authors = db.query(Author).all()
    return {"authors": authors}


@router.get("/{author_id}", response_model=schemas.AuthorSchema)
def get_author(
    author_id: int,
    authenticated_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.put("/{author_id}", response_model=schemas.AuthorSchema)
def edit_author(
    author_id: int,
    author: schemas.AuthorCreateSchema,
    authenticated_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    author_db = db.query(Author).filter(Author.id == author_id).first()
    if not author_db:
        raise HTTPException(status_code=404, detail="Author not found")
    author_db.name = author.name
    db.commit()
    db.refresh(author_db)
    return author_db

