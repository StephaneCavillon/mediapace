from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BookBase(BaseModel):
  title: str
  author: Optional[str] = None
  pages: Optional[int] = None
  isbn: Optional[str] = None
  google_books_id: Optional[str] = None
  cover_url: Optional[str] = None

class BookCreate(BookBase):
  pass

class BookUpdate(BaseModel):
  title: Optional[str] = None
  author: Optional[str] = None
  pages: Optional[int] = None
  current_page: Optional[int] = None
  isbn: Optional[str] = None
  cover_url: Optional[str] = None
  ended_at: Optional[datetime] = None

class BookResponse(BookBase):
  id: int
  current_page: Optional[int] = None
  type: str
  created_at: datetime
  updated_at: datetime
  ended_at: Optional[datetime] = None

  class Config:
    from_attributes = True
