from fastapi import HTTPException

from src.models import Book
from src.schemas import BookCreate, BookUpdate
from src.services.books_service import books_service


def test_book_creation(context):
  book_data = BookCreate(
    title='1984', author='George Orwell', pages=328, user=str(context['test_user'].id)
  )
  book = books_service.create(book_data, context['test_user'].id)

  created_book = len(Book.select())
  assert created_book == 1
  assert book.title == '1984'
  assert book.author == 'George Orwell'
  assert book.pages == 328
  assert book.user.id == context['test_user'].id


def test_book_update(context):
  book_data = BookCreate(
    title='1984', author='George Orwell', pages=328, user=str(context['test_user'].id)
  )
  book = books_service.create(book_data, context['test_user'].id)

  updated_book = books_service.update(
    book.id, context['test_user'], BookUpdate(pages=330)
  )

  assert updated_book.title == '1984'
  assert updated_book.author == 'George Orwell'
  assert updated_book.pages == 330
  assert updated_book.user.id == context['test_user'].id


def test_book_delete(context):
  book_data = BookCreate(
    title='1984', author='George Orwell', pages=328, user=str(context['test_user'].id)
  )
  book = books_service.create(book_data, str(context['test_user'].id))

  deleted_book = books_service.delete(book.id, context['test_user'])

  assert deleted_book == 1
  assert len(Book.select()) == 0


def test_book_get(context):
  book_data = BookCreate(
    title='1984', author='George Orwell', pages=328, user=str(context['test_user'].id)
  )
  book = books_service.create(book_data, context['test_user'].id)

  gotten_book = books_service.get(book.id, context['test_user'])

  assert gotten_book.title == '1984'
  assert gotten_book.author == 'George Orwell'
  assert gotten_book.pages == 328
  assert gotten_book.user.id == context['test_user'].id


def test_user_book_list(context, seed_books):
  listed_books = books_service.list(str(context['test_user'].id))

  assert len(listed_books) == 3
  assert listed_books[0].title == 'Test Book 1'
  assert listed_books[0].author == 'Test Author 1'
  assert listed_books[0].pages == 100
  assert listed_books[0].user.id == context['test_user'].id
  assert listed_books[1].title == 'Test Book 2'
  assert listed_books[1].author == 'Test Author 2'
  assert listed_books[1].pages == 200
  assert listed_books[1].user.id == context['test_user'].id


def test_fail_update(context):
  try:
    books_service.update(999, context['test_user'], BookUpdate(pages=330))
  except HTTPException as e:
    assert e.status_code == 404
    assert e.detail == 'Book not found'


def test_fail_delete(context):
  try:
    books_service.delete(999, context['test_user'])
  except HTTPException as e:
    assert e.status_code == 404
    assert e.detail == 'Book not found'
