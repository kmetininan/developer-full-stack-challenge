from sqlalchemy.orm import Session
from schema import BookCreate, AuthorCreate, AuthorRead, Book

import models

def get_authors(q: str, db: Session, skip: int = 0, limit: int = 100):
    if len(q) == 0:
        return db.query(models.Author).offset(skip).limit(limit).all()
    else:
        search_tag = "%{}%".format(q)
        return db.query(models.Author).filter(models.Author.name.like(search_tag)).offset(skip).limit(limit).all()

def create_author(db: Session, author: AuthorCreate):
    item = {"name": author.name}
    db_item: AuthorRead = models.Author(**item)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    for i in author.books:
        book = {
            "name": i['name'],
            "pages_count": int(i['pages_count']),
            "author_id": db_item.id
        }
        create_bulk_books(db, book)
    return db_item

def update_author(db: Session, author_id: int, author: AuthorCreate):
    db_item: AuthorCreate = db.query(models.Author).filter(models.Author.id == author_id).first()
    if db_item:
        db_item.name = author.name
        db.commit()
        db.refresh(db_item)
        delete_all_books_for_author(db, author_id)
        for i in author.books:
            book = {
                'name': i['name'],
                'pages_count': int(i['pages_count']),
                'author_id': author_id
            }
            create_bulk_books(db, book)
        return author

def delete_author(db: Session, author_id: int):
    db_item = db.query(models.Author).filter(models.Author.id==author_id).first()
    db.delete(db_item)
    db.commit()
    return {"success": True}

def get_books(q: str, db: Session, skip: int = 0, limit: int = 100):
    if len(q) == 0:
        return db.query(models.Book).offset(skip).limit(limit).all()
    else:
        search_tag = "%{}%".format(q)
        return db.query(models.Book).filter(models.Book.name.like(search_tag)).offset(skip).limit(limit).all()

def create_book(db: Session, book: Book):
    item = {"name": book.name, "pages_count": book.pages_count, "author_id": book.author_id}
    db_item = models.Book(**item)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def create_bulk_books(db: Session, book: Book):
    db_item = models.Book(**book)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_book(db: Session, book_id: int, book: Book):
    db_item: Book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_item:
        db_item.name = book.name
        db_item.pages_count = book.pages_count
        db_item.author_id = book.author_id
        db.commit()
        db.refresh(db_item)
        return book

def delete_book(db: Session, book_id: int):
    db_item = db.query(models.Book).filter(models.Book.id==book_id).first()
    db.delete(db_item)
    db.commit()
    return {"success": True}

def delete_all_books_for_author(db: Session, author_id: int):
    db_items = db.query(models.Book).filter(models.Book.author_id==author_id)
    for db_item in db_items:
        db.delete(db_item)
    db.commit()
    return {"success": True}