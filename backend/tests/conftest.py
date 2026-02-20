import pytest
from fastapi.testclient import TestClient
from peewee import SqliteDatabase

from src.auth.security import create_access_token
from src.models import Book, Game, User

test_db = SqliteDatabase('file::memory:?cache=shared', uri=True)


def seed_users():
  test_user = User.create(
    username='test', email='test@test.com', password='test', role='user'
  )
  test_admin = User.create(
    username='admin', email='admin@admin.com', password='admin', role='admin'
  )
  return {'test_user': test_user, 'test_admin': test_admin}


@pytest.fixture(autouse=True)  # autouse equivalent de beforeEach et afterEach
def context():
  # 1. lier le modele a la base de données
  test_db.bind([Book, User, Game], bind_refs=False, bind_backrefs=False)
  test_db.connect()
  # 2. créer les tables
  test_db.create_tables([Book, User, Game])

  # 3. créer un utilisateur de test
  ctx = seed_users()

  # 4. exécuter le test
  yield ctx

  # 5. nettoyer après le test
  test_db.drop_tables([Book, User, Game])
  test_db.close()


@pytest.fixture
def auth_user(context):
  from src.main import app

  token = create_access_token(data={'sub': str(context['test_user'].id)})
  client = TestClient(app)
  client.headers = {'Authorization': f'Bearer {token}'}
  return client


@pytest.fixture
def auth_admin(context):
  from src.main import app

  token = create_access_token(data={'sub': str(context['test_admin'].id)})
  client = TestClient(app)
  client.headers = {'Authorization': f'Bearer {token}'}
  return client


@pytest.fixture
def seed_books(context):
  books = [
    Book.create(
      title='Test Book 1',
      author='Test Author 1',
      pages=100,
      user=context['test_user'].id,
    ),
    Book.create(
      title='Test Book 2',
      author='Test Author 2',
      pages=200,
      user=context['test_user'].id,
    ),
    Book.create(
      title='Test Book 3',
      author='Test Author 3',
      pages=300,
      user=context['test_user'].id,
    ),
    Book.create(
      title='Test Book 4',
      author='Test Author 4',
      pages=400,
      user=context['test_admin'].id,
    ),
    Book.create(
      title='Test Book 5',
      author='Test Author 5',
      pages=500,
      user=context['test_admin'].id,
    ),
  ]
  return books


@pytest.fixture
def seed_games(context):
  games = [
    Game.create(
      title='Test Game 1',
      platform='PC',
      completion_time=10.5,
      time_played=5.0,
      user=context['test_user'].id,
    ),
    Game.create(
      title='Test Game 2',
      platform='PS5',
      completion_time=20.0,
      time_played=15.0,
      user=context['test_user'].id,
    ),
    Game.create(
      title='Test Game 3',
      platform='Xbox',
      completion_time=30.0,
      time_played=25.0,
      user=context['test_user'].id,
    ),
    Game.create(
      title='Test Game 4',
      platform='Switch',
      completion_time=40.0,
      time_played=35.0,
      user=context['test_admin'].id,
    ),
    Game.create(
      title='Test Game 5',
      platform='PC',
      completion_time=50.0,
      time_played=45.0,
      user=context['test_admin'].id,
    ),
  ]
  return games
