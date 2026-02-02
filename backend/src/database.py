from peewee import Model
from playhouse.sqlite_ext import SqliteExtDatabase

db = SqliteExtDatabase(
  'data/db.sqlite',
  pragmas={
    'journal_mode': 'wal',
    'cache_size': -1024 * 64,
    'foreign_keys': 1,
    'ignore_check_constraints': 0,
    'synchronous': 1,
  },
)


class BaseModel(Model):
  class Meta:
    database = db
