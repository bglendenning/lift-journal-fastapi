from typing import Annotated

from fastapi import APIRouter, Depends
from lift_journal_data.crud import LiftDAO
from lift_journal_data.schemas.lift import LiftSchema
from lift_journal_data.schemas.user import UserReadSchema

from lift_journal_fastapi import db
from lift_journal_fastapi.authentication import get_token_user

router = APIRouter()


@router.get("/", tags=["Lifts"])
def get_lifts(
        user: Annotated[UserReadSchema, Depends(get_token_user)],
        session=Depends(db.get_session),
) -> list[LiftSchema]:
    db_lifts = LiftDAO(session).get_all()

    return [LiftSchema.parse_obj(db_lift) for db_lift in db_lifts]
