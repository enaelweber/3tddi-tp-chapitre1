from enum import StrEnum

from pydantic import BaseModel, EmailStr, Field


class FieldEnum(StrEnum):
    INFORMATIQUE = "Informatique"
    MATHEMATIQUES = "Mathématiques"
    PHYSIQUE = "Physique"
    CHIMIE = "Chimie"


class StudentBase(BaseModel):
    firstName: str = Field(min_length=2)
    lastName: str = Field(min_length=2)
    email: EmailStr
    grade: float = Field(ge=0, le=20)  # adapte l'échelle si besoin
    field: FieldEnum


class StudentCreate(StudentBase):
    pass


class StudentUpdate(StudentBase):
    pass  # PUT = remplacement complet


class Student(StudentBase):
    id: int
