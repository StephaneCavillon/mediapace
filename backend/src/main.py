from fastapi import APIRouter, FastAPI

from src.database import db
from src.models import Book, Game, User
from src.routers import books, games, users

app = FastAPI(
  title='Mediapace API', description='Mediapace API', version='0.0.1', debug=True
)

db.create_tables([User, Book, Game])


# Route
@app.get('/health')
def health():
  return {'status': 'OK'}


# Login
@app.get('/login')
def login():
  return {'message': 'Login'}


# Dashboard
@app.get('/dashboard')
def dashboard():
  # @todo: implement dashboard
  return {'message': 'Welcome to the dashboard'}


# Routers
api_router = APIRouter(prefix='/api')
api_router.include_router(books.router)
api_router.include_router(games.router)
api_router.include_router(users.router)

app.include_router(api_router)
