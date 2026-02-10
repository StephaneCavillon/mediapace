from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.auth.security import decode_access_token
from src.models import User

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
  token = credentials.credentials
  payload = decode_access_token(token)

  if not payload:
    raise HTTPException(status_code=401, detail='Invalid token')

  user_id = payload.get('sub')
  if not user_id:
    raise HTTPException(status_code=401, detail='Invalid token')

  try:
    user = User.get(User.id == user_id)
  except User.DoesNotExist:
    raise HTTPException(status_code=401, detail='User not found') from None

  return user


def get_current_admin(current_user: User = Depends(get_current_user)):
  if current_user.role != 'admin':
    raise HTTPException(status_code=403, detail='Admin access required')

  return current_user
