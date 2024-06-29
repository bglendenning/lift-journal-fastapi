from fastapi import APIRouter, Response, status
from lift_journal_data.schemas import requests

router = APIRouter()


@router.post("/user/register", status_code=status.HTTP_202_ACCEPTED)
def register(user: requests.UserRegister):
    return Response(status_code=status.HTTP_202_ACCEPTED)
