from app.seed_data import SEED_STUDENTS

# GET


def test_get_students_returns_200_and_list(client):
    response = client.get("/students")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_students_returns_SEED_STUDENTS(client):
    data = client.get("/students").json()
    assert len(data) == len(SEED_STUDENTS)
    emails = {s["email"] for s in data}
    expected = {s["email"] for s in SEED_STUDENTS}
    assert emails == expected


def test_get_student_by_valid_id(client):
    response = client.get("/students/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_student_by_nonexistent_id(client):
    response = client.get("/students/9999")
    assert response.status_code == 404


def test_get_student_by_invalid_id(client):
    response = client.get("/students/abc")
    assert response.status_code == 422


# POST


def test_post_student_valid_data(client):
    payload = {
        "firstName": "Alice",
        "lastName": "Durelle",
        "email": "alice.durelle@example.com",
        "grade": 14.0,
        "field": "Informatique",
    }
    response = client.post("/students", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["firstName"] == "Alice"


def test_post_student_missing_required_field(client):
    payload = {
        "lastName": "Dupont",
        "email": "jean.dupont@example.com",
        "grade": 14.0,
        "field": "Informatique",
    }  # firstName manquant
    response = client.post("/students", json=payload)
    assert response.status_code == 422


def test_post_student_invalid_grade(client):
    payload = {
        "firstName": "Jean",
        "lastName": "Dupont",
        "email": "jean.dupont@example.com",
        "grade": 25,
        "field": "Informatique",
    }
    response = client.post("/students", json=payload)
    assert response.status_code == 422


def test_post_student_duplicate_email(client):
    payload = {
        "firstName": "Autre",
        "lastName": "Personne",
        "email": SEED_STUDENTS[0]["email"],
        "grade": 10.0,
        "field": "Informatique",
    }
    response = client.post("/students", json=payload)
    assert response.status_code == 409


# PUT


def test_put_student_valid_data(client):
    payload = {
        "firstName": "Alice",
        "lastName": "Martin",
        "email": "alice.updated@example.com",
        "grade": 17.0,
        "field": "Informatique",
    }
    response = client.put("/students/1", json=payload)
    assert response.status_code == 200
    assert response.json()["email"] == "alice.updated@example.com"


def test_put_student_nonexistent_id(client):
    payload = {
        "firstName": "XXX",
        "lastName": "YYY",
        "email": "x.y@example.com",
        "grade": 10.0,
        "field": "Informatique",
    }
    response = client.put("/students/9999", json=payload)
    assert response.status_code == 404


# DELETE


def test_delete_student_valid_id(client):
    response = client.delete("/students/1")
    assert response.status_code == 200


def test_delete_student_nonexistent_id(client):
    response = client.delete("/students/9999")
    assert response.status_code == 404


# stats, search


def test_get_stats(client):
    response = client.get("/students/stats")
    assert response.status_code == 200
    data = response.json()
    for key in ("totalStudents", "averageGrade", "studentsByField", "bestStudent"):
        assert key in data


def test_search_students(client):
    query = SEED_STUDENTS[0]["firstName"]
    response = client.get(f"/students/search?q={query}")
    assert response.status_code == 200
    data = response.json()
    assert any(query.lower() in s["firstName"].lower() for s in data)
