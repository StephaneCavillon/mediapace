def test_get_empty_books_list(auth_user):
  response = auth_user.get('/api/books/')
  assert response.status_code == 200
  assert response.json() == []


def test_get_user_books(auth_user, seed_books):
  response = auth_user.get('/api/books/')
  books = response.json()
  assert response.status_code == 200
  assert len(books) == 3
  titles = [b['title'] for b in books]
  assert 'Test Book 1' in titles
  assert 'Test Book 2' in titles
  assert 'Test Book 3' in titles


def test_get_all_books(auth_admin, seed_books):
  response = auth_admin.get('/api/books/admin/all')
  assert response.status_code == 200
  books = response.json()
  assert len(books) == 5


def test_wrong_user_on_admin_endpoints(auth_user, seed_books):
  response = auth_user.get('/api/books/admin/all')
  assert response.status_code == 403
  response = auth_user.get('/api/books/admin/{book_id}')
  assert response.status_code == 403


def test_wrong_user_on_book(auth_user, seed_books):
  admin_book = seed_books[3]
  response = auth_user.get(f'/api/books/{admin_book.id}')
  assert response.status_code == 404


def test_create_book(auth_user):
  book = {
    'title': 'Test Book',
    'author': 'Test Author',
    'pages': 100,
  }
  response = auth_user.post('/api/books/', json=book)
  assert response.status_code == 200
  book_response = response.json()
  assert book_response['id'] == 1
  assert book_response['title'] == 'Test Book'
  assert book_response['author'] == 'Test Author'
  assert book_response['pages'] == 100


def test_update_book(auth_user, seed_books):
  book = seed_books[0]
  response = auth_user.patch(
    f'/api/books/{book.id}', json={'title': 'Test Book Updated'}
  )
  assert response.status_code == 200
  book_response = response.json()
  assert book_response['title'] == 'Test Book Updated'


def test_delete_book(auth_user, seed_books):
  book = seed_books[0]
  response = auth_user.delete(f'/api/books/{book.id}')
  assert response.status_code == 200
  assert response.json() == 1
  response = auth_user.get(f'/api/books/{book.id}')
  assert response.status_code == 404


def test_admin_get_user_book(auth_admin, seed_books):
  book = seed_books[0]
  response = auth_admin.get(f'/api/books/admin/{book.id}')
  assert response.status_code == 200
  book_response = response.json()
  assert book_response['id'] == book.id
  assert book_response['title'] == book.title
  assert book_response['author'] == book.author
  assert book_response['pages'] == book.pages
