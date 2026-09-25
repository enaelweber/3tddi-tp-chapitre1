from pydantic import BaseModel, EmailStr, Field

class StudentBase(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    grade: float = Field(ge=0, le=20)  # adapte l'échelle si besoin
    field: str  # filière

class StudentCreate(StudentBase):
    pass

class StudentUpdate(StudentBase):
    pass  # PUT = remplacement complet

class Student(StudentBase):
    id: int