import os
from datetime import datetime, timedelta, timezone
from typing_extensions import Annotated

import jwt
from fastapi import status, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from lift_journal_data.crud import UserDAO
from lift_journal_data.schemas.user import UserReadSchema
from passlib.context import CryptContext

from lift_journal_fastapi import db

SECRET_KEY = os.environ["LIFT_JOURNAL_FASTAPI_SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token/create")


def create_access_token(data: dict):
    data = data.copy()
    expires = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expires})
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def get_token_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except InvalidTokenError:
        raise credentials_exception

    email: str = payload.get("sub")

    if not email:
        raise credentials_exception

    db_user = UserDAO(db.SessionLocal()).get_for_email(email)

    if not db_user:
        raise credentials_exception

    return UserReadSchema(email=db_user.email, id=db_user.id)


def authenticate_user(form_data: OAuth2PasswordRequestForm):
    db_user = UserDAO(db.SessionLocal()).get_for_email(form_data.username)

    if db_user and pwd_context.verify(form_data.password, db_user.password):
        return UserReadSchema(email=db_user.email, id=db_user.id)
