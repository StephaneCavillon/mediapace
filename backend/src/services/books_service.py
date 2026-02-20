from fastapi import HTTPException

from src.models import Book, User
from src.schemas import BookCreate, BookUpdate


class BooksService:
  # list all books for a user
  def list(self, user: str):
    return Book.select().where(Book.user == user).order_by(Book.title)

  # list all books for admin
  def list_all(self):
    return Book.select()

  def get(self, book_id: int, user: User):
    try:
      if user.role == 'admin':
        return Book.get_by_id(book_id)
      else:
        return Book.get(Book.id == book_id, Book.user == user.id)
    except Book.DoesNotExist:
      raise HTTPException(status_code=404, detail='Book not found') from None

  def create(self, data: BookCreate, user: str):
    book = data.model_dump()
    book['user'] = user
    return Book.create(**book)

  def update(self, book_id: int, user: User, data: BookUpdate):
    q = Book.update(**data.model_dump(exclude_unset=True)).where(
      Book.id == book_id, Book.user == user.id
    )
    row_updated = q.execute()
    if row_updated == 0:
      raise HTTPException(status_code=404, detail='Book not found')
    return Book.get_by_id(book_id)

  def delete(self, book_id: int, user: User):
    q = Book.delete().where(Book.id == book_id, Book.user == user.id)
    row_deleted = q.execute()
    if row_deleted == 0:
      raise HTTPException(status_code=404, detail='Book not found')
    return row_deleted


books_service = BooksService()
