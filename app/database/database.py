# app/database/database.py

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# app/database/database.py

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
Session = scoped_session(SessionLocal)

# This context manager ensures proper session handling within each request
@contextmanager
def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class BookModel(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    publication_year = Column(Integer)

    from app.models.review import Review
    reviews = relationship("ReviewModel", back_populates="book")


class ReviewModel(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    text_review = Column(Text)
    rating = Column(Float)
    book_id = Column(Integer, ForeignKey("books.id"))

    book = relationship("BookModel", back_populates="reviews")



def get_db_engine():
    return engine
