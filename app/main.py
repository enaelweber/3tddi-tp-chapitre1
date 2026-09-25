from fastapi import FastAPI
from app.routers import students

app = FastAPI(title="Students API")
app.include_router(students.router)

@app.get("/")
def root():
    return {"status": "ok"}