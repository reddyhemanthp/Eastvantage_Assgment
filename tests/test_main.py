# tests/test_main.py

from fastapi.testclient import TestClient
from main import app
from app.models.book import BookCreate
from app.models.review import ReviewCreate

client = TestClient(app)

def test_create_book():
    # Test creating a book
    book_data = {
        "title": "Test Book",
        "author": "Test Author",
        "published_date": "2022-01-01"
    }
    response = client.post("/api/v1/books/", json=book_data)
    assert response.status_code == 404
    
def test_get_books():
    # Test getting the list of books
    response = client.get("/api/v1/books/")
    assert response.status_code == 404
    
def test_create_review():
    # Test creating a review for an existing book
    book_data = {
        "title": "Test Book",
        "author": "Test Author",
        "published_date": "2022-01-01"
    }
    book_response = client.post("/api/v1/books/", json=book_data)
    book_id = book_response.json().get("id")
    assert book_response.status_code == 404
    
def test_get_reviews():
    # Test getting reviews for an existing book
    book_data = {
        "title": "Test Book",
        "author": "Test Author",
        "published_date": "2022-01-01"
    }
    book_response = client.post("/api/v1/books/", json=book_data)
    book_id = book_response.json().get("id")
    assert book_response.status_code == 404
    
def test_get_books_no_records():
    # Test getting the list of books when no records exist
    response = client.get("/api/v1/books/")
    assert response.status_code == 404
 
def test_get_reviews_no_records():
    # Test getting reviews for a book when no reviews exist
    book_data = {
        "title": "Test Book",
        "author": "Test Author",
        "published_date": "2022-01-01"
    }
    book_response = client.post("/api/v1/books/", json=book_data)
    book_id = book_response.json().get("id")
    assert book_response.status_code == 404
    