from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_session, get_current_user
from app.core.security import get_password_hash
from app.crud.users import crud_user
from app.schemas.user import UserCreate, UserInDB, UserOut, UserUpdate
from app.schemas.customer import CustomerUpdate
from app.models.users import User
from app.models.customers import Customer
from app.models.address import Address


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserOut)
def create_user(user_in: UserCreate, session: Session = Depends(get_session)):
    """
    Create new user.
    """

    # Pengecekan jika field kosong
    if not user_in.email or not user_in.password:
        raise HTTPException(
            status_code=400,
            detail="Field in body must not be empty.",
        )

    # Pengecekan jika pengguna sudah ada
    user = crud_user.get(session, email=user_in.email)
    if user is not None:
        raise HTTPException(
            status_code=409,
            detail="The user with this email already exists in the system",
        )

    hashed_password = get_password_hash(user_in.password)
    obj_in = UserInDB(**user_in.dict(exclude="password"), password=hashed_password)
    return crud_user.create(session, obj_in)


@router.put(
    "/{user_id}/", response_model=UserOut, dependencies=[Depends(get_current_user)]
)
def update_user(
    user_id: UUID, user_in: UserUpdate, session: Session = Depends(get_session)
):
    user = crud_user.get(session, user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    try:
        user = crud_user.update(
            session,
            db_obj=user,
            obj_in={
                **user_in.dict(exclude={"password"}, exclude_none=True),
                "hashed_password": get_password_hash(user_in.password),
            },
        )
    except IntegrityError:
        raise HTTPException(
            status_code=409, detail="User with this username already exits"
        )
    return user


@router.delete("/{user_id}/", status_code=204)
def delete_user(
    user_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    user = crud_user.get(session, id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if current_user.id == user_id:
        raise HTTPException(status_code=403, detail="User can't delete itself")
    crud_user.delete(session, db_obj=user)


@router.get("/me/", response_model=CustomerUpdate)
def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    customer_data = (
        session.query(Customer).filter(Customer.user_id == current_user.user_id).first()
    )
    address_data = (
        session.query(Address)
        .filter(Address.customer_id == customer_data.customer_id)
        .first()
    )

    data = {
        "email": current_user.email,
        "user_id": current_user.user_id,
        "customer": {
            "first_name": customer_data.first_name,
            "last_name": customer_data.last_name,
            "address": address_data,
        },
    }
    return current_user
