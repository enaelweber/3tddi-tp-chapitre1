from fastapi import APIRouter, Depends, HTTPException, status
from app.models import Student, StudentCreate, StudentUpdate
from app.repository import StudentRepository, get_repository

router = APIRouter(prefix="/students", tags=["students"])


@router.get("/stats")
def get_stats(repo: StudentRepository = Depends(get_repository)):
    students = repo.list_all()
    if not students:
        return {
            "totalStudents": 0,
            "averageGrade": 0,
            "studentsByField": {},
            "bestStudent": None,
        }
    grades = [s.grade for s in students]
    by_field: dict[str, int] = {}
    for s in students:
        by_field[s.field] = by_field.get(s.field, 0) + 1
    return {
        "totalStudents": len(students),
        "averageGrade": round(sum(grades) / len(grades), 2),
        "studentsByField": by_field,
        "bestStudent": max(grades),
    }


@router.get("/search")
def search_students(q: str = "", repo: StudentRepository = Depends(get_repository)):
    if not q.strip():
        raise HTTPException(status_code=400, detail="Query parameter 'q' is required")
    return repo.search(q)


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


@router.put("/{student_id}", response_model=Student)
def update_student(
    student_id: int, data: StudentUpdate, repo: StudentRepository = Depends(get_repository)
):
    if not repo.get(student_id):
        raise HTTPException(status_code=404, detail="Student not found")
    if repo.email_exists(data.email, exclude_id=student_id):
        raise HTTPException(status_code=409, detail="Email already exists")
    return repo.update(student_id, data)


@router.delete("/{student_id}")
def delete_student(student_id: int, repo: StudentRepository = Depends(get_repository)):
    if not repo.delete(student_id):
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}
