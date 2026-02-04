from datetime import datetime

from peewee import AutoField, CharField, DateTimeField, FloatField

from src.database import BaseModel


class Game(BaseModel):
  id = AutoField()
  title = CharField(null=False)
  platform = CharField(null=True)
  completion_time = FloatField(null=True)
  time_played = FloatField(null=True, default=0)
  cover_url = CharField(null=True)
  created_at = DateTimeField(null=False, default=datetime.now)
  updated_at = DateTimeField(null=True)
  type = CharField(null=False, default='game')
  ended_at = DateTimeField(null=True)
