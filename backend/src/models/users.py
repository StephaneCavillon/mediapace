from datetime import datetime

from peewee import CharField, DateTimeField, UUIDField

from src.database import BaseModel


class User(BaseModel):
  id = UUIDField(primary_key=True)
  username = CharField(unique=True, null=False)
  email = CharField(unique=True, null=False)
  password = CharField(null=False)
  avatar_url = CharField(null=True)
  created_at = DateTimeField(null=False, default=datetime.now)
  updated_at = DateTimeField(null=True)

  def save(self, *args, **kwargs):
    # Mettre à jour updated_at à chaque sauvegarde
    if self.id is not None:  # Si c'est une mise à jour (pas une création)
      self.updated_at = datetime.now()
    return super().save(*args, **kwargs)
