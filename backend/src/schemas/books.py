from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BookBase(BaseModel):
  title: str
  author: str | None = None
  pages: int | None = None
  isbn: str | None = None
  google_books_id: str | None = None
  cover_url: str | None = None


class BookCreate(BookBase):
  pass


class BookUpdate(BaseModel):
  title: str | None = None
  author: str | None = None
  pages: int | None = None
  current_page: int | None = None
  isbn: str | None = None
  cover_url: str | None = None
  ended_at: datetime | None = None


class BookResponse(BookBase):
  id: int
  current_page: int | None = None
  type: str
  created_at: datetime
  updated_at: datetime
  ended_at: datetime | None = None

  model_config = ConfigDict(from_attributes=True, extra='ignore')
