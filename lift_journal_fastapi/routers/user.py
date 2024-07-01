from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from lift_journal_data.crud import UserDAO
from lift_journal_data.schemas.user import UserSchema
from passlib.context import CryptContext

from lift_journal_fastapi import db
from lift_journal_fastapi.authentication import create_access_token, oauth2_scheme
from lift_journal_fastapi.schemas.user import TokenSchema, UserCreateSchema

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/")
def read_root(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"Hello": "World"}


@router.post("/token/create")
async def create_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> TokenSchema:
    user = UserSchema(email=form_data.username, password=form_data.password)
    db_user = UserDAO(db.SessionLocal()).get_for_email(user.email)

    if not pwd_context.verify(form_data.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token({"sub": user.email})

    return TokenSchema(access_token=access_token, token_type="bearer")


@router.post("/create", status_code=status.HTTP_202_ACCEPTED)
async def create_user(user: UserCreateSchema):
    user.password2 = user.password = pwd_context.hash(user.password)
    UserDAO(db.SessionLocal()).create(user)

    return Response(status_code=status.HTTP_202_ACCEPTED)
