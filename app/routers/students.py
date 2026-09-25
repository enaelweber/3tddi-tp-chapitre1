from fastapi import APIRouter, Depends, HTTPException, status
from app.models import Student, StudentCreate, StudentUpdate
from app.repository import StudentRepository, get_repository

router = APIRouter(prefix="/students", tags=["students"])

@router.get("", response_model=list[Student])
def list_students(repo: StudentRepository = Depends(get_repository)):
    return repo.list_all()