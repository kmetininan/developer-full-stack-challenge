from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    password = Column(String)
    username = Column(String)

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    
    books = relationship("Book", back_populates="author", cascade="all,delete")
    

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    pages_count = Column(Integer, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    
    author = relationship("Author",  back_populates="books")
