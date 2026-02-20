from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_serializer


class GameBase(BaseModel):
  title: str
  user: str
  platform: str | None = None
  completion_time: float | None = None
  time_played: float | None = None
  cover_url: str | None = None


class GameCreate(GameBase):
  user: str


class GameUpdate(BaseModel):
  title: str | None = None
  platform: str | None = None
  completion_time: float | None = None
  time_played: float | None = None
  cover_url: str | None = None
  ended_at: datetime | None = None


class GameResponse(GameBase):
  id: int
  user: str | object  # type: ignore[assignment]
  type: str
  created_at: datetime
  updated_at: datetime | None = None
  ended_at: datetime | None = None

  model_config = ConfigDict(from_attributes=True, extra='ignore')

  @field_serializer('user')
  def serialize_user(self, user):
    if hasattr(user, 'id'):
      return str(user.id)
    return str(user)
