from fastapi import FastAPI

from lift_journal_fastapi.routers import user
from lift_journal_fastapi.routers import lift_set

tags_metadata = [
    {
        "name": "Users",
        "description": "Operations on users, including authentication."
    },
    {
        "name": "Lift Sets",
        "description": "Operations on lift sets."
    },
]

app = FastAPI(openapi_tags=tags_metadata)

app.include_router(user.router, prefix="/users")
app.include_router(lift_set.router, prefix="/lift-sets")
