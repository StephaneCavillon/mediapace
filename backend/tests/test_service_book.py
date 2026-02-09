from src.models import Book
from src.schemas import BookCreate
from src.services.books_service import books_service

# objet pydantic


# test de création
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
