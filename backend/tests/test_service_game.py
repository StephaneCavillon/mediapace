from fastapi import HTTPException

from src.models import Game, User
from src.schemas import GameCreate, GameUpdate
from src.services.games_service import games_service


def test_game_creation(context):
  game_data = GameCreate(
    title='The Legend of Zelda',
    platform='Nintendo Switch',
    completion_time=50.5,
    user=str(context['test_user'].id),
  )
  game = games_service.create(game_data)

  created_game = len(Game.select())
  assert created_game == 1
  assert game.title == 'The Legend of Zelda'
  assert game.platform == 'Nintendo Switch'
  assert game.completion_time == 50.5
  assert game.user.id == context['test_user'].id


def test_game_update(context):
  game_data = GameCreate(
    title='The Legend of Zelda',
    platform='Nintendo Switch',
    completion_time=50.5,
    user=str(context['test_user'].id),
  )
  game = games_service.create(game_data)

  updated_game = games_service.update(
    game.id, context['test_user'], GameUpdate(time_played=25.0)
  )

  assert updated_game.title == 'The Legend of Zelda'
  assert updated_game.platform == 'Nintendo Switch'
  assert updated_game.time_played == 25.0
  assert updated_game.user.id == context['test_user'].id


def test_game_delete(context):
  game_data = GameCreate(
    title='The Legend of Zelda',
    platform='Nintendo Switch',
    completion_time=50.5,
    user=str(context['test_user'].id),
  )
  game = games_service.create(game_data)

  deleted_game = games_service.delete(game.id, context['test_user'])

  assert deleted_game == 1
  assert len(Game.select()) == 0


def test_game_get(context):
  game_data = GameCreate(
    title='The Legend of Zelda',
    platform='Nintendo Switch',
    completion_time=50.5,
    user=str(context['test_user'].id),
  )
  game = games_service.create(game_data)

  gotten_game = games_service.get(game.id, context['test_user'])

  assert gotten_game.title == 'The Legend of Zelda'
  assert gotten_game.platform == 'Nintendo Switch'
  assert gotten_game.completion_time == 50.5
  assert gotten_game.user.id == context['test_user'].id


def test_user_game_list(context):
  test_user_2 = User.create(
    username='test2', email='test2@test.com', password='test2', role='user'
  )
  game_data = [
    GameCreate(
      title='The Legend of Zelda',
      platform='Nintendo Switch',
      completion_time=50.5,
      user=str(context['test_user'].id),
    ),
    GameCreate(
      title='Elden Ring',
      platform='PC',
      completion_time=80.0,
      user=str(context['test_user'].id),
    ),
    GameCreate(
      title='God of War',
      platform='PlayStation 5',
      completion_time=30.0,
      user=str(test_user_2.id),
    ),
  ]

  for game in game_data:
    games_service.create(game)

  listed_games = games_service.list(str(context['test_user'].id))

  assert len(listed_games) == 2
  assert listed_games[0].title == 'Elden Ring'
  assert listed_games[0].platform == 'PC'
  assert listed_games[0].completion_time == 80.0
  assert listed_games[0].user.id == context['test_user'].id
  assert listed_games[1].title == 'The Legend of Zelda'
  assert listed_games[1].platform == 'Nintendo Switch'
  assert listed_games[1].completion_time == 50.5
  assert listed_games[1].user.id == context['test_user'].id


def test_fail_update(context):
  try:
    games_service.update(999, context['test_user'], GameUpdate(time_played=25.0))
  except HTTPException as e:
    assert e.status_code == 404
    assert e.detail == 'Game not found'


def test_fail_delete(context):
  try:
    games_service.delete(999, context['test_user'])
  except HTTPException as e:
    assert e.status_code == 404
    assert e.detail == 'Game not found'
