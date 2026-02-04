from datetime import datetime

import pytest
from pydantic import ValidationError

from src.schemas.books import BookBase, BookCreate, BookResponse, BookUpdate


def test_book_base():
  book = BookBase(title='1984', author='George Orwell', pages=328)

  assert book.title == '1984'
  assert book.author == 'George Orwell'
  assert book.pages == 328


def test_book_create():
  book = BookCreate(title='1984', author='George Orwell', pages=328)

  assert book.title == '1984'
  assert book.author == 'George Orwell'
  assert book.pages == 328
  assert 'created_at' not in str(book)
  assert 'updated_at' not in str(book)


def test_book_create_failure():
  with pytest.raises(ValidationError) as err:
    BookCreate(author='George Orwell', pages=328)

  assert 'title' in str(err.value)


def test_book_update():
  book = BookUpdate(title='1984', author='George Orwell', pages=328, isbn='1234567890')

  assert book.title == '1984'
  assert book.author == 'George Orwell'
  assert book.pages == 328
  assert book.isbn == '1234567890'
  assert 'created_at' not in str(book)
  assert 'updated_at' not in str(book)


def test_book_response():
  book = BookResponse(
    id=1,
    title='1984',
    author='George Orwell',
    pages=328,
    isbn='1234567890',
    cover_url='https://example.com/cover.jpg',
    created_at=datetime.now(),
    updated_at=datetime.now(),
    ended_at=None,
    type='book',
  )

  assert book.title == '1984'
  assert book.author == 'George Orwell'
  assert book.pages == 328
  assert 'created_at' in str(book)
  assert 'updated_at' in str(book)
  assert 'ended_at' in str(book)
