from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from lift_journal_data.crud import UserDAO
from passlib.context import CryptContext

from lift_journal_fastapi import db
from lift_journal_fastapi.authentication import authenticate_user, create_access_token
from lift_journal_fastapi.schemas.user import TokenSchema, UserCreateMatchSchema

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/token/create", tags=["Users"])
async def create_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> TokenSchema:
    user = authenticate_user(form_data)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token({"sub": user.email, "id": user.id})

    return TokenSchema(access_token=access_token, token_type="bearer")


@router.post("/create", status_code=status.HTTP_202_ACCEPTED, tags=["Users"])
async def create_user(user: UserCreateMatchSchema) -> Response:
    user.password2 = user.password = pwd_context.hash(user.password)
    UserDAO(db.SessionLocal()).create(user)

    return Response(status_code=status.HTTP_202_ACCEPTED)
