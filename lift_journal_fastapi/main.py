from fastapi import FastAPI

from lift_journal_fastapi.routers import user

app = FastAPI()

app.include_router(user.router, prefix="/user")


@app.get("/")
def read_root():
    return {"Hello": "World"}
