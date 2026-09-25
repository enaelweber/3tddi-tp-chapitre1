from fastapi import APIRouter, Depends, HTTPException, status
from app.models import Student, StudentCreate, StudentUpdate
from app.repository import StudentRepository, get_repository

router = APIRouter(prefix="/students", tags=["students"])

@router.get("", response_model=list[Student])
def list_students(repo: StudentRepository = Depends(get_repository)):
    return repo.list_all()

@router.get("/{student_id}", response_model=Student)
def get_student(student_id: int, repo: StudentRepository = Depends(get_repository)):
    student = repo.get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.post("", response_model=Student, status_code=status.HTTP_201_CREATED)
def create_student(data: StudentCreate, repo: StudentRepository = Depends(get_repository)):
    if repo.email_exists(data.email):
        raise HTTPException(status_code=409, detail="Email already exists")
    return repo.create(data)