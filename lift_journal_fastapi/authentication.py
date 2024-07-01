from datetime import datetime, timedelta, timezone
from typing_extensions import Annotated

import jwt
from fastapi import status, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from lift_journal_data.crud import UserDAO

from lift_journal_fastapi import db
from lift_journal_fastapi.schemas.user import UserReadSchema

SECRET_KEY = "secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/token/create")


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

    user = UserDAO(db.SessionLocal()).get_for_email(email)

    if not user:
        raise credentials_exception

    return UserReadSchema(email=user.email)
