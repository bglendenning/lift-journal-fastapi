from fastapi import APIRouter, Response, status
from lift_journal_data.crud import create_user
from lift_journal_data.schemas import requests

router = APIRouter()


@router.post("/user/create", status_code=status.HTTP_202_ACCEPTED)
def create_user(user: requests.UserCreate):
    user = create_user(user)

    return Response(status_code=status.HTTP_202_ACCEPTED)
