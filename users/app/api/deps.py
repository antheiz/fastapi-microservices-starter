from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import SessionLocal
from app.core.security import ALGORITHM
from app.crud.users import crud_user
from app.schemas.token import TokenPayload
from app.models.users import User


oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_token_data(token: str = Depends(oauth2)) -> TokenPayload:
    try:
        secret_key = settings.SECRET_KEY.get_secret_value()
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return token_data


def get_current_user(
    token: str = Depends(get_token_data),
    session: Session = Depends(get_session),
):
    user = crud_user.get(session, user_id=token.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
