from datetime import datetime

from peewee import AutoField, CharField, DateTimeField, FloatField, ForeignKeyField

from src.database import BaseModel
from src.models.users import User


class Game(BaseModel):
  id = AutoField()
  user = ForeignKeyField(
    User, backref='games', null=False
  )  # relation avec l'utilisateur
  title = CharField(null=False)
  platform = CharField(null=True)
  completion_time = FloatField(null=True)
  time_played = FloatField(null=True, default=0)
  cover_url = CharField(null=True)
  created_at = DateTimeField(null=False, default=datetime.now)
  updated_at = DateTimeField(null=True)
  type = CharField(null=False, default='game')
  ended_at = DateTimeField(null=True)
