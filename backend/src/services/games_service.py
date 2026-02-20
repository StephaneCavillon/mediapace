from fastapi import HTTPException

from src.models import Game, User
from src.schemas.games import GameCreate, GameUpdate


class GamesService:
  # list all Games for a user
  def list(self, user: str):
    return Game.select().where(Game.user == user).order_by(Game.title)

  # list all Games for admin
  def list_all(self):
    return Game.select()

  def get(self, game_id: int, user: User):
    try:
      if user.role == 'admin':
        return Game.get_by_id(game_id)
      else:
        return Game.get(Game.id == game_id, Game.user == user.id)
    except Game.DoesNotExist:
      raise HTTPException(status_code=404, detail='Game not found') from None

  def create(self, data: GameCreate, user: str):
    game = data.model_dump()
    game['user'] = user
    return Game.create(**game)

  def update(self, game_id: int, user: User, data: GameUpdate):
    q = Game.update(**data.model_dump(exclude_unset=True)).where(
      Game.id == game_id, Game.user == user.id
    )
    row_updated = q.execute()
    if row_updated == 0:
      raise HTTPException(status_code=404, detail='Game not found')
    return Game.get_by_id(game_id)

  def delete(self, game_id: int, user: User):
    q = Game.delete().where(Game.id == game_id, Game.user == user.id)
    row_deleted = q.execute()
    if row_deleted == 0:
      raise HTTPException(status_code=404, detail='Game not found')
    return row_deleted


games_service = GamesService()
