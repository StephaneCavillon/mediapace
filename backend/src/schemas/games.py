from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class GameBase(BaseModel):
  title: str
  platform: Optional[str] = None
  completion_time: Optional[float] = None
  time_played: Optional[float] = None
  cover_url: Optional[str] = None

class GameCreate(GameBase):
  pass

class GameUpdate(Basemodel):
  title = Optional[str] = None
  platform = Optional[str] = None
  completion_time = Optional[float] = None
  time_played = Optional[float]
  cover_url = Optional[str] = None
  ended_at = Optional[datetime]

class GameResponse(GameBase):
  id: int
  time_played: Optional[float] = None
  created_at: datetime
  updated_at: Optional[datetime] = None
  ended_at: Optional[datetime] = None

  class Config:
    from_attributes = True