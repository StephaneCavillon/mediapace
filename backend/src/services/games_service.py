from fastapi import HTTPException

from src.models import Game
from src.schemas.games import GameCreate, GameUpdate


class GamesService:
  # list all Games for a user
  def list(self, user: str):
    return Game.select().where(Game.user == user).order_by(Game.title)

  # list all Games for admin
  def list_all(self):
    return Game.select()

  def get(self, game_id: int):
    return Game.get_by_id(game_id)

  def create(self, data: GameCreate):
    return Game.create(**data.model_dump())

  def update(self, game_id: int, data: GameUpdate):
    q = Game.update(**data.model_dump(exclude_unset=True)).where(Game.id == game_id)
    row_updated = q.execute()
    if row_updated == 0:
      raise HTTPException(status_code=404, detail='Game not found')
    return Game.get_by_id(game_id)

  def delete(self, game_id: int):
    q = Game.delete().where(Game.id == game_id)
    row_deleted = q.execute()
    if row_deleted == 0:
      raise HTTPException(status_code=404, detail='Game not found')
    return row_deleted


games_service = GamesService()
