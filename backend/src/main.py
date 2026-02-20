from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI, HTTPException, Request

from src.auth.security import create_access_token, verify_password
from src.database import db
from src.models import Book, Game, User
from src.routers import books, games, users
from src.schemas.auth import LoginRequest, TokenResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
  # Startup: create tables
  db.create_tables([User, Book, Game])
  yield
  # Shutdown: close database
  db.close()


app = FastAPI(
  title='Mediapace API',
  description='Mediapace API',
  version='0.0.1',
  debug=True,
  lifespan=lifespan,
)


# Route
@app.get('/health')
def health():
  return {'status': 'OK'}


# Login
@app.post('/login', response_model=TokenResponse)
def login(credentials: LoginRequest):
  try:
    user = User.get(User.email == credentials.email)
  except User.DoesNotExist:
    raise HTTPException(status_code=401, detail='Invalid credentials') from None

  if not verify_password(credentials.password, user.password):
    raise HTTPException(status_code=401, detail='Invalid credentials')

  token = create_access_token({'sub': user.id})
  return {'access_token': token, 'token_type': 'bearer'}


# Dashboard
@app.get('/dashboard')
def dashboard(request: Request):
  # @todo: implement dashboard
  return {'message': 'Welcome to the dashboard'}


# Routers
api_router = APIRouter(prefix='/api')
api_router.include_router(books.router)
api_router.include_router(games.router)
api_router.include_router(users.router)

app.include_router(api_router)
