from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from lift_journal_data.crud import UserDAO
from lift_journal_data.schemas.user import UserSchema
from passlib.context import CryptContext

from lift_journal_fastapi import db
from lift_journal_fastapi.schemas.user import TokenSchema, UserCreateSchema

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/token/create")
async def create_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> TokenSchema:
    with db.SessionLocal() as session:
        user = UserSchema(email=form_data.username, password=form_data.password)
        db_user = UserDAO(session).get_for_email(user.email)

        if not pwd_context.verify(form_data.password, db_user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return TokenSchema(access_token="", token_type="")


@router.post("/create", status_code=status.HTTP_202_ACCEPTED)
async def create_user(user: UserCreateSchema):
    user.password2 = user.password = pwd_context.hash(user.password)

    with db.SessionLocal() as session:
        UserDAO(session).create(user)

    return Response(status_code=status.HTTP_202_ACCEPTED)
