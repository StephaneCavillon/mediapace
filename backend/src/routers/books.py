from fastapi import APIRouter

from src.schemas.books import BookCreate, BookResponse, BookUpdate

router = APIRouter(prefix='/books', tags=['books'])


@router.get('/', response_model=list[BookResponse])
def list_books():
  # @todo: implement list books
  return {'message': 'List of books'}


@router.get('/{book_id}', response_model=BookResponse)
def get_book(book_id: int):
  # @todo: implement get book
  return {'message': f'Book {book_id}'}


@router.post('/', response_model=BookResponse)
def create_book(book: BookCreate):
  # @todo: implement create book
  return {'message': 'Book created'}


@router.patch('/{book_id}', response_model=BookResponse)
def update_book(book_id: int, book: BookUpdate):
  # @todo: implement update book
  return {'message': f'Book {book_id} updated'}


@router.delete('/{book_id}', response_model=BookResponse)
def delete_book(book_id: int):
  # @todo: implement delete book
  return {'message': f'Book {book_id} deleted'}
