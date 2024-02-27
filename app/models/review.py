from pydantic import BaseModel

class ReviewBase(BaseModel):
    text_review: str
    rating: float

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    book_id: int

    class Config:
        orm_mode = True
