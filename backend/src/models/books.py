from datetime import datetime
from backend.src.database import BaseModel
from peewee import AutoField, CharField, IntegerField, DateTimeField

class Book(BaseModel):
    id = AutoField()
    isbn = CharField(unique=True, null=True)
    google_books_id = CharField(unique=True, null=True) # null False à vérifier si on laisse creér un livre sans qu'il soit dans google_books
    title = CharField(null=False)
    author = CharField(null=True)
    pages = IntegerField(null=True)
    current_page = IntegerField(default=0)
    cover_url = CharField(null=True)
    created_at = DateTimeField(null=True, default=datetime.datetime.now)
    updated_at = DateTimeField(null=False, default=datetime.datetime.now)
    type = CharField(null=False, default='book')
    ended_at = DateTimeField(null=True)
