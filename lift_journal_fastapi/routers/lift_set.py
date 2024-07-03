from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from lift_journal_data.crud import LiftSetDAO
from lift_journal_data.schemas.user import UserReadSchema
from lift_journal_data.schemas.lift_set import LiftSetBaseSchema, LiftSetReadSchema

from lift_journal_fastapi import db
from lift_journal_fastapi.authentication import get_token_user

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def post_lift_set(
        lift_set: LiftSetBaseSchema,
        user: Annotated[UserReadSchema, Depends(get_token_user)]
) -> LiftSetReadSchema:
    lift_set = LiftSetBaseSchema(
        lift_id=lift_set.lift_id,
        repetitions=lift_set.repetitions,
        weight=lift_set.weight,
        date_performed=lift_set.date_performed,
        time_performed=lift_set.time_performed,
    )
    db_lift_set = LiftSetDAO(db.SessionLocal(), user.id).create(lift_set)

    if not db_lift_set:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="LiftSet not created")

    return LiftSetReadSchema.from_orm(db_lift_set)


@router.get("/{lift_set_id}")
def get_lift_set(
        lift_set_id: int,
        user: Annotated[UserReadSchema, Depends(get_token_user)]
) -> LiftSetReadSchema:
    db_lift_set = LiftSetDAO(db.SessionLocal(), user.id).get_for_lift_set_id(lift_set_id)

    if not db_lift_set:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="LiftSet not found")

    return LiftSetReadSchema.parse_obj(db_lift_set)


@router.get("/")
def get_lift_sets(user: Annotated[UserReadSchema, Depends(get_token_user)]) -> list[LiftSetReadSchema]:
    db_lift_sets = LiftSetDAO(db.SessionLocal(), user.id).get_for_user_id()

    return [LiftSetReadSchema.parse_obj(db_lift_set) for db_lift_set in db_lift_sets]
