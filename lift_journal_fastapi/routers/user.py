from fastapi import APIRouter
from lift_journal_data.schemas import request

router = APIRouter()


@router.post("/user/register")
def register(user: request.User):
    return user
