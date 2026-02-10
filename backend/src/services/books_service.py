from fastapi import HTTPException

from src.models import Book
from src.schemas import BookCreate, BookUpdate


class BooksService:
  # list all books for a user
  def list(self, user: str):
    return Book.select().where(Book.user == user).order_by(Book.title)

  # list all books for admin
  def list_all(self):
    return Book.select()

  def get(self, book_id: int):
    return Book.get_by_id(book_id)

  def create(self, data: BookCreate):
    return Book.create(**data.model_dump())

  def update(self, book_id: int, data: BookUpdate):
    q = Book.update(**data.model_dump(exclude_unset=True)).where(Book.id == book_id)
    row_updated = q.execute()
    if row_updated == 0:
      raise HTTPException(status_code=404, detail='Book not found')
    return Book.get_by_id(book_id)

  def delete(self, book_id: int):
    q = Book.delete().where(Book.id == book_id)
    row_deleted = q.execute()
    if row_deleted == 0:
      raise HTTPException(status_code=404, detail='Book not found')
    return row_deleted


books_service = BooksService()
