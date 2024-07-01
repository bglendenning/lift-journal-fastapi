from fastapi import APIRouter, Response, status
from lift_journal_data.crud import UserDAO

from lift_journal_fastapi import db
from lift_journal_fastapi.schemas import UserCreateSchema

router = APIRouter()


@router.post("/user/create", status_code=status.HTTP_202_ACCEPTED)
def create_user(user: UserCreateSchema):
    with db.SessionLocal() as session:
        UserDAO(session).create(user)

    return Response(status_code=status.HTTP_202_ACCEPTED)
