from fastapi import FastAPI

from lift_journal_fastapi.routers import user
from lift_journal_fastapi.routers import lift_set

app = FastAPI()

app.include_router(user.router, prefix="/user")
app.include_router(lift_set.router, prefix="/lift-sets")
