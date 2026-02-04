from fastapi import APIRouter

from src.schemas.games import GameCreate, GameResponse, GameUpdate

router = APIRouter(prefix='/games', tags=['games'])


@router.get('/', response_model=GameResponse)
def list_games():
  # @todo: implement list games
  return {'message': 'List of games'}


@router.get('/{game_id}', response_model=GameResponse)
def get_game(game_id: int):
  # @todo: implement get game
  return {'message': f'Game {game_id}'}


@router.post('/', response_model=GameResponse)
def create_game(game: GameCreate):
  # @todo: implement create game
  return {'message': 'Game created'}


@router.patch('/{game_id}', response_model=GameResponse)
def update_game(game_id: int, game: GameUpdate):
  # @todo: implement update game
  return {'message': f'Game {game_id} updated'}


@router.delete('/{game_id}', response_model=GameResponse)
def delete_game(game_id: int):
  # @todo: implement delete game
  return {'message': f'Game {game_id} deleted'}
