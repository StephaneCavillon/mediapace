from fastapi import APIRouter, Depends, HTTPException

from src.auth.dependencies import get_current_admin, get_current_user
from src.models import User
from src.schemas.books import BookBase, BookResponse, BookUpdate
from src.services.books_service import books_service

router = APIRouter(prefix='/books', tags=['books'])


@router.get('/', response_model=list[BookResponse])
def list_user_books(current_user: User = Depends(get_current_user)):
  return books_service.list(current_user.id)


@router.get('/{book_id}', response_model=BookResponse)
def get_books(book_id: int, current_user: User = Depends(get_current_user)):
  book = books_service.get(book_id, current_user)
  return book


@router.get('/admin/all', response_model=list[BookResponse])
def list_all_books(current_user: User = Depends(get_current_admin)):
  return books_service.list_all()


@router.get('/admin/{book_id}', response_model=BookResponse)
def get_all_books(book_id: int, current_user: User = Depends(get_current_admin)):
  return books_service.get(book_id, current_user)


@router.post('/', response_model=BookResponse)
def create_book(book: BookBase, current_user: User = Depends(get_current_user)):
  return books_service.create(book, user=str(current_user.id))


@router.patch('/{book_id}', response_model=BookResponse)
def update_book(
  book_id: int, book: BookUpdate, current_user: User = Depends(get_current_user)
):
  updated = books_service.update(book_id, current_user, book)
  if not updated:
    raise HTTPException(status_code=404, detail='Book not found')
  return updated


@router.delete('/{book_id}')
def delete_book(book_id: int, current_user: User = Depends(get_current_user)):
  deleted = books_service.delete(book_id, current_user)
  if not deleted:
    raise HTTPException(status_code=404, detail='Book not found')
  return deleted
