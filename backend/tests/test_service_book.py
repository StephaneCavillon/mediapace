from fastapi import HTTPException

from src.models import Book, User
from src.schemas import BookCreate, BookUpdate
from src.services.books_service import books_service


def test_book_creation(context):
  book_data = BookCreate(
    title='1984', author='George Orwell', pages=328, user=str(context['test_user'].id)
  )
  book = books_service.create(book_data)

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
  book = books_service.create(book_data)

  updated_book = books_service.update(book.id, BookUpdate(pages=330))

  assert updated_book.title == '1984'
  assert updated_book.author == 'George Orwell'
  assert updated_book.pages == 330
  assert updated_book.user.id == context['test_user'].id


def test_book_delete(context):
  book_data = BookCreate(
    title='1984', author='George Orwell', pages=328, user=str(context['test_user'].id)
  )
  book = books_service.create(book_data)

  deleted_book = books_service.delete(book.id)

  assert deleted_book == 1
  assert len(Book.select()) == 0


def test_book_get(context):
  book_data = BookCreate(
    title='1984', author='George Orwell', pages=328, user=str(context['test_user'].id)
  )
  book = books_service.create(book_data)

  gotten_book = books_service.get(book.id)

  assert gotten_book.title == '1984'
  assert gotten_book.author == 'George Orwell'
  assert gotten_book.pages == 328
  assert gotten_book.user.id == context['test_user'].id


def test_user_book_list(context):
  test_user_2 = User.create(
    username='test2', email='test2@test.com', password='test2', role='user'
  )
  book_data = [
    BookCreate(
      title='1984', author='George Orwell', pages=328, user=str(context['test_user'].id)
    ),
    BookCreate(
      title='Animal Farm',
      author='George Orwell',
      pages=112,
      user=str(context['test_user'].id),
    ),
    BookCreate(
      title='The Great Gatsby',
      author='F. Scott Fitzgerald',
      pages=180,
      user=str(test_user_2.id),
    ),
  ]

  for book in book_data:
    books_service.create(book)

  listed_books = books_service.list(str(context['test_user'].id))

  assert len(listed_books) == 2
  assert listed_books[0].title == '1984'
  assert listed_books[0].author == 'George Orwell'
  assert listed_books[0].pages == 328
  assert listed_books[0].user.id == context['test_user'].id
  assert listed_books[1].title == 'Animal Farm'
  assert listed_books[1].author == 'George Orwell'
  assert listed_books[1].pages == 112
  assert listed_books[1].user.id == context['test_user'].id


def test_fail_update():
  try:
    books_service.update(999, BookUpdate(pages=330))
  except HTTPException as e:
    assert e.status_code == 404
    assert e.detail == 'Book not found'


def test_fail_delete():
  try:
    books_service.delete(999)
  except HTTPException as e:
    assert e.status_code == 404
    assert e.detail == 'Book not found'
