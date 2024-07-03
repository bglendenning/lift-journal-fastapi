from typing import Annotated

from fastapi import APIRouter, Depends
from lift_journal_data.crud import LiftSetDAO
from lift_journal_data.schemas.user import UserReadSchema
from lift_journal_data.schemas.lift_set import LiftSetBaseSchema, LiftSetCreateSchema

from lift_journal_fastapi import db
from lift_journal_fastapi.authentication import get_token_user

router = APIRouter()


@router.post("/")
def post_set(lift_set: LiftSetBaseSchema, user: Annotated[UserReadSchema, Depends(get_token_user)]):
    lift_set = LiftSetCreateSchema(
        user_id=user.id,
        lift_id=lift_set.lift_id,
        repetitions=lift_set.repetitions,
        weight=lift_set.weight,
        date_performed=lift_set.date_performed,
        time_performed=lift_set.time_performed,
    )
    db_lift_set = LiftSetDAO(db.SessionLocal()).create(lift_set)

    if db_lift_set:
        return LiftSetBaseSchema.from_orm(db_lift_set)
