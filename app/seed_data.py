from app.models import StudentCreate

SEED_STUDENTS = [
    StudentCreate(firstName="Jean", lastName="Dupont", email="jean.dupont@example.com", grade=15.5, field="Informatique"),
    StudentCreate(firstName="Marie", lastName="Martin", email="marie.martin@example.com", grade=12.0, field="Mathématiques"),
    StudentCreate(firstName="Ahmed", lastName="Benali", email="ahmed.benali@example.com", grade=17.25, field="Marketing"),
    StudentCreate(firstName="Sophie", lastName="Leroy", email="sophie.leroy@example.com", grade=9.5, field="Physique"),
    StudentCreate(firstName="Lucas", lastName="Moreau", email="lucas.moreau@example.com", grade=14.0, field="Informatique"),
]