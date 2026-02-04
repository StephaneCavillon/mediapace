from uuid import uuid4

import pytest
from peewee import IntegrityError, SqliteDatabase

from src.models.books import Book

# base de donnée de test
db_test = SqliteDatabase(':memory:')


@pytest.fixture(autouse=True)  # autouse equivalent de beforeEach et afterEach
def setup_database():
  # 1. Lier le modèle à la base de test
  db_test.bind([Book])

  # 2. Créer les tables
  db_test.create_tables([Book])

  # 3. Exécuter le test
  yield

  # 4. Nettoyer après le test
  db_test.drop_tables([Book])
  db_test.close()


def test_book_creation():
  book = Book.create(title='1984', author='George Orwell', pages=328, user_id=1)

  assert book.id is not None
  assert book.title == '1984'
  assert book.author == 'George Orwell'
  assert book.pages == 328
  assert book.current_page == 0
  assert book.type == 'book'
  assert book.user_id == 1
  assert book.created_at is not None
  assert book.updated_at is None


def test_book_unicity_on_isbn():
  Book.create(
    title='1984', author='George Orwell', pages=328, user_id=1, isbn='1234567890'
  )
  with pytest.raises(IntegrityError):
    Book.create(
      title='1984', author='George Orwell', pages=328, user_id=1, isbn='1234567890'
    )


def test_book_read():
  book = Book.create(
    title='1984', author='George Orwell', pages=328, isbn='1234567890', user_id=uuid4()
  )
  assert Book.get_by_id(book.id).title == '1984'
  assert Book.get_by_id(book.id).author == 'George Orwell'
  assert Book.get_by_id(book.id).pages == 328
  assert Book.get_by_id(book.id).isbn == '1234567890'


def test_book_update():
  book = Book.create(
    title='1984', author='George Orwell', pages=328, isbn='1234567890', user_id=uuid4()
  )
  assert Book.get_by_id(book.id).title == '1984'

  # update 1
  # book.update(title='1985').where(book.id == book.id).execute()

  # update 2
  book.title = '1985'
  book.save()

  updated = Book.get_by_id(book.id)

  assert updated.title == '1985'
  assert updated.updated_at is not None


def test_book_delete():
  book = Book.create(
    title='1984', author='George Orwell', pages=328, isbn='1234567890', user_id=uuid4()
  )
  book_id = book.id
  assert Book.get_by_id(book_id).title == '1984'
  Book.delete_by_id(book_id)
  with pytest.raises(Book.DoesNotExist):  # a voir si on garde ce comportement d'erreur
    Book.get_by_id(book_id)
