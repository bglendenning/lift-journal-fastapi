from lift_journal_data.schemas.lift_set import LiftSetReadSchema
from pydantic import BaseModel


class LiftSetCollectionResponseSchema(BaseModel):
    items: list[LiftSetReadSchema]
    count: int
    pages: int
