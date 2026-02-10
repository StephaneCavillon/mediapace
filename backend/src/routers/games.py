from fastapi import APIRouter, Depends, HTTPException

from src.auth.dependencies import get_current_admin, get_current_user
from src.models import User
from src.schemas.games import GameCreate, GameResponse, GameUpdate
from src.services.games_service import games_service

router = APIRouter(prefix='/games', tags=['games'])


@router.get('/', response_model=list[GameResponse])
def list_user_games(current_user: User = Depends(get_current_user)):
  return games_service.list(str(current_user.id))


@router.get('/{game_id}', response_model=GameResponse)
def get_games(game_id: int, current_user: User = Depends(get_current_user)):
  game = games_service.get(game_id)
  if current_user.role != 'admin' and game.user.id != current_user.id:
    raise HTTPException(status_code=403, detail='Forbidden')
  return game


@router.get('/admin/all', response_model=list[GameResponse])
def list_all_games(current_user: User = Depends(get_current_admin)):
  return games_service.list_all()


@router.get('/admin/{game_id}', response_model=GameResponse)
def get_all_games(game_id: int, current_user: User = Depends(get_current_admin)):
  return games_service.get(game_id)


@router.post('/', response_model=GameResponse)
def create_game(game: GameCreate, current_user: User = Depends(get_current_user)):
  return games_service.create(game)


@router.patch('/{game_id}', response_model=GameResponse)
def update_game(
  game_id: int, game: GameUpdate, current_user: User = Depends(get_current_user)
):
  updated = games_service.update(game_id, current_user, game)
  if not updated:
    raise HTTPException(status_code=404, detail='Game not found')
  return updated


@router.delete('/{game_id}', response_model=GameResponse)
def delete_game(game_id: int, current_user: User = Depends(get_current_user)):
  deleted = games_service.delete(game_id, current_user)
  if not deleted:
    raise HTTPException(status_code=404, detail='Game not found')
  return deleted
