# app/api/main.py

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from app.models.book import Book, BookCreate
from app.models.review import Review, ReviewCreate
from app.database.database import BookModel, ReviewModel, get_db, get_session, get_db_engine, Base
from sqlalchemy.exc import IntegrityError
from app.email import send_confirmation_email

main_router = APIRouter()

# Add a startup event to create tables
@main_router.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=get_db_engine())


@main_router.post("/books/", response_model=Book)
async def create_book(book: BookCreate, db: Session = Depends(get_session)):
    try:
        with db as session:  # Use the session as a context manager
            db_book = BookModel(**book.dict())
            session.add(db_book)
            session.commit()
            session.refresh(db_book)
            return db_book
    except Exception as e:
        # Note: The context manager will automatically handle rollback if an exception occurs
        raise HTTPException(status_code=500, detail=str(e))


@main_router.get("/books/", response_model=list[Book])
async def get_books(db: Session = Depends(get_db)):
    try:
        with db as session:
            books = session.query(BookModel).all()
            if not books:
                raise HTTPException(status_code=404, detail="No records found.")
            return books
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@main_router.post("/reviews/{book_id}", response_model=Review)
async def create_review(book_id: int, review: ReviewCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_session)):
    try:
        with db as session:
            # Check if the specified book exists
            existing_book = session.query(BookModel).filter(BookModel.id == book_id).first()
            if not existing_book:
                raise HTTPException(status_code=404, detail="Book not found.")

            db_review = ReviewModel(**review.dict(), book_id=book_id)
            session.add(db_review)
            session.commit()
            session.refresh(db_review)

            # Trigger background task to send a confirmation email
            background_tasks.add_task(send_confirmation_email, db_review.text_review)

            return db_review
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@main_router.get("/reviews/{book_id}", response_model=list[Review])
async def get_reviews(book_id: int, db: Session = Depends(get_session)):
    try:
        with db as session:
            # Check if the specified book exists
            existing_book = session.query(BookModel).filter(BookModel.id == book_id).first()
            if not existing_book:
                raise HTTPException(status_code=404, detail="Book not found.")

            reviews = session.query(ReviewModel).filter(ReviewModel.book_id == book_id).all()
            if not reviews:
                raise HTTPException(status_code=404, detail="No reviews found for the specified book.")
            return reviews
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))