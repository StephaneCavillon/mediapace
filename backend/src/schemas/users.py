from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
  username: str
  email: str
  password: str
  avatar_url: str | None = None


class UserCreate(UserBase):
  pass


class UserUpdate(UserBase):
  pass


class UserResponse(UserBase):
  id: str
  created_at: datetime
  updated_at: datetime

  model_config = ConfigDict(from_attributes=True)
