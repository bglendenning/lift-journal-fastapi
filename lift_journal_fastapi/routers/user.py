from fastapi import APIRouter, Response, status
from lift_journal_data.crud import UserDAO
from passlib.context import CryptContext

from lift_journal_fastapi import db
from lift_journal_fastapi.schemas import UserCreateSchema

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/create", status_code=status.HTTP_202_ACCEPTED)
async def create_user(user: UserCreateSchema):
    user.password2 = user.password = pwd_context.hash(user.password)

    with db.SessionLocal() as session:
        UserDAO(session).create(user)

    return Response(status_code=status.HTTP_202_ACCEPTED)
