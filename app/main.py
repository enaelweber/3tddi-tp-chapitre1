from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import students
from app.repository import repository
from app.seed_data import SEED_STUDENTS

@asynccontextmanager
async def lifespan(app: FastAPI):
    repository.seed(SEED_STUDENTS)
    yield

app = FastAPI(title="Students API", lifespan=lifespan)
app.include_router(students.router)

@app.get("/")
def root():
    return {"status": "ok"}