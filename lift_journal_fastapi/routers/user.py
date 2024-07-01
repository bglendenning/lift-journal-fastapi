from fastapi import APIRouter, Response, status
from lift_journal_data import crud
from lift_journal_data.schemas.user import UserSchema

from lift_journal_fastapi import db

router = APIRouter()


@router.post("/user/create", status_code=status.HTTP_202_ACCEPTED)
def create_user(user: UserSchema):
    with db.SessionLocal() as session:
        crud.create_user(session, user)

    return Response(status_code=status.HTTP_202_ACCEPTED)
