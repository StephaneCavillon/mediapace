from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_serializer


class BookBase(BaseModel):
  title: str
  author: str | None = None
  pages: int | None = None
  isbn: str | None = None
  google_books_id: str | None = None
  cover_url: str | None = None


class BookCreate(BookBase):
  user: str


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
  user: str | object
  current_page: int | None = None
  type: str
  created_at: datetime
  updated_at: datetime | None = None
  ended_at: datetime | None = None

  model_config = ConfigDict(from_attributes=True, extra='ignore')

  @field_serializer('user')
  def serialize_user(self, user):
    if hasattr(user, 'id'):
      return str(user.id)
    return str(user)
