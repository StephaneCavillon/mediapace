def test_get_empty_games_list(auth_user):
  response = auth_user.get('/api/games/')
  assert response.status_code == 200
  assert response.json() == []


def test_get_user_games(auth_user, seed_games):
  response = auth_user.get('/api/games/')
  games = response.json()
  assert response.status_code == 200
  assert len(games) == 3
  titles = [g['title'] for g in games]
  assert 'Test Game 1' in titles
  assert 'Test Game 2' in titles
  assert 'Test Game 3' in titles


def test_get_all_games(auth_admin, seed_games):
  response = auth_admin.get('/api/games/admin/all')
  assert response.status_code == 200
  games = response.json()
  assert len(games) == 5


def test_wrong_user_on_admin_endpoints(auth_user, seed_games):
  response = auth_user.get('/api/games/admin/all')
  assert response.status_code == 403
  response = auth_user.get('/api/games/admin/{game_id}')
  assert response.status_code == 403


def test_wrong_user_on_game(auth_user, seed_games):
  admin_game = seed_games[3]
  response = auth_user.get(f'/api/games/{admin_game.id}')
  assert response.status_code == 404


def test_create_game(auth_user):
  game = {
    'title': 'Test Game',
    'platform': 'PC',
    'completion_time': 10.5,
    'time_played': 5.0,
    'user': str(auth_user),
  }
  response = auth_user.post('/api/games/', json=game)
  assert response.status_code == 200
  game_response = response.json()
  assert game_response['id'] == 1
  assert game_response['title'] == 'Test Game'
  assert game_response['platform'] == 'PC'
  assert game_response['completion_time'] == 10.5
  assert game_response['time_played'] == 5.0


def test_update_game(auth_user, seed_games):
  game = seed_games[0]
  response = auth_user.patch(
    f'/api/games/{game.id}', json={'title': 'Test Game Updated'}
  )
  assert response.status_code == 200
  game_response = response.json()
  assert game_response['title'] == 'Test Game Updated'


def test_delete_game(auth_user, seed_games):
  game = seed_games[0]
  response = auth_user.delete(f'/api/games/{game.id}')
  assert response.status_code == 200
  assert response.json() == 1
  response = auth_user.get(f'/api/games/{game.id}')
  assert response.status_code == 404


def test_admin_get_user_game(auth_admin, seed_games):
  game = seed_games[0]
  response = auth_admin.get(f'/api/games/admin/{game.id}')
  assert response.status_code == 200
  game_response = response.json()
  assert game_response['id'] == game.id
  assert game_response['title'] == game.title
  assert game_response['platform'] == game.platform
  assert game_response['completion_time'] == game.completion_time
