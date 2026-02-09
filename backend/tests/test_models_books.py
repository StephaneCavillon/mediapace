import pytest
from peewee import IntegrityError

from src.models.books import Book


def test_book_creation(context):
  book = Book.create(
    title='1984', author='George Orwell', pages=328, user=context['test_user'].id
  )

  assert book.id is not None
  assert book.title == '1984'
  assert book.author == 'George Orwell'
  assert book.pages == 328
  assert book.current_page == 0
  assert book.type == 'book'
  assert book.user.id == context['test_user'].id
  assert book.created_at is not None
  assert book.updated_at is None


def test_book_unicity_on_isbn(context):
  Book.create(
    title='1984',
    author='George Orwell',
    pages=328,
    user=context['test_user'].id,
    isbn='1234567890',
  )
  with pytest.raises(IntegrityError):
    Book.create(
      title='1984',
      author='George Orwell',
      pages=328,
      user=context['test_user'].id,
      isbn='1234567890',
    )


def test_book_read(context):
  book = Book.create(
    title='1984',
    author='George Orwell',
    pages=328,
    isbn='1234567890',
    user=context['test_user'].id,
  )
  assert Book.get_by_id(book.id).title == '1984'
  assert Book.get_by_id(book.id).author == 'George Orwell'
  assert Book.get_by_id(book.id).pages == 328
  assert Book.get_by_id(book.id).isbn == '1234567890'


def test_book_update(context):
  book = Book.create(
    title='1984',
    author='George Orwell',
    pages=328,
    isbn='1234567890',
    user=context['test_user'].id,
  )
  assert Book.get_by_id(book.id).title == '1984'

  book.title = '1985'
  book.save()

  updated = Book.get_by_id(book.id)

  assert updated.title == '1985'
  assert updated.updated_at is not None


def test_book_delete(context):
  book = Book.create(
    title='1984',
    author='George Orwell',
    pages=328,
    isbn='1234567890',
    user=context['test_user'].id,
  )
  book_id = book.id
  assert Book.get_by_id(book_id).title == '1984'
  Book.delete_by_id(book_id)
  with pytest.raises(Book.DoesNotExist):  # a voir si on garde ce comportement d'erreur
    Book.get_by_id(book_id)
