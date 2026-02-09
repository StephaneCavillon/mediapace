import pytest
from peewee import SqliteDatabase

from src.models import Book, Game, User

test_db = SqliteDatabase(':memory:')


def seed_db():
  test_user = User.create(
    username='test', email='test@test.com', password='test', role='user'
  )
  return {'test_user': test_user}


@pytest.fixture(autouse=True)  # autouse equivalent de beforeEach et afterEach
def context():
  # 1. lier le modele a la base de données
  test_db.bind([Book, User, Game], bind_refs=False, bind_backrefs=False)
  # 2. créer les tables
  test_db.create_tables([Book, User, Game])

  # 3. créer un utilisateur de test
  ctx = seed_db()

  # 4. exécuter le test
  yield ctx

  # 5. nettoyer après le test
  test_db.drop_tables([Book, User, Game])
  test_db.close()
