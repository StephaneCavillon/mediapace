from datetime import datetime
from backend.src.database import BaseModel
from peewee import AutoField, CharField, DateTimeField

class Game(BaseModel):
    id = AutoField()
    title = CharField(null=False)
    platform = CharField(null=True)
    completion_time = FloatField(null=True)
    time_played = FloatField(null=True, default=0)
    cover_url = CharField(null=True)
    created_at = DateTimeField(null=True, default=datetime.datetime.now)
    updated_at = DateTimeField(null=False, default=datetime.datetime.now)
    type = CharField(null=False, default='game')
    ended_at = DateTimeField(null=True)