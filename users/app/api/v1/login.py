from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_session
from app.core.security import authenticate, create_access_token
from app.schemas.token import Token

router = APIRouter(tags=["Users"])


@router.post("/login/", response_model=Token)
def login(
    data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = authenticate(session, email=data.username, password=data.password)
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return {"access_token": create_access_token(user), "token_type": "bearer"}
