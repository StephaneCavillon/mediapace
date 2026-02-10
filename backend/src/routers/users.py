from fastapi import APIRouter

from src.schemas.users import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/', response_model=UserResponse)
def create_user(user: UserCreate):
  # @todo: implement create user
  return {'message': f'User {user.username}'}


@router.patch('/{user_id}', response_model=UserResponse)
def update_user(user_id: str, user: UserUpdate):
  # @todo: implement update user
  return {'message': f'User {user_id}'}


@router.get('/', response_model=list[UserResponse])
def list_users():
  # @todo: implement list users for admin only
  return {'message': 'List of users'}


@router.get('/{user_id}', response_model=UserResponse)
def get_user(user_id: str):
  # @todo: implement get user for admin only
  return {'message': f'User {user_id}'}


@router.delete('/{user_id}', response_model=UserResponse)
def delete_user(user_id: str):
  # @todo: implement delete user for admin only
  return {'message': f'User {user_id}'}
