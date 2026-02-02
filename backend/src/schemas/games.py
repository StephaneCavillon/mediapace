from datetime import datetime

from pydantic import BaseModel, ConfigDict


class GameBase(BaseModel):
  title: str
  platform: str | None = None
  completion_time: float | None = None
  time_played: float | None = None
  cover_url: str | None = None


class GameCreate(GameBase):
  pass


class GameUpdate(BaseModel):
  title: str | None = None
  platform: str | None = None
  completion_time: float | None = None
  time_played: float | None = None
  cover_url: str | None = None
  ended_at: datetime | None = None


class GameResponse(GameBase):
  id: int
  time_played: float | None = None
  created_at: datetime
  updated_at: datetime | None = None
  ended_at: datetime | None = None

  model_config = ConfigDict(from_attributes=True, extra='ignore')
