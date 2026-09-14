import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fastapi.testclient import TestClient

import app as app_module

client = TestClient(app_module.app)


def test_student_signup_requires_teacher_login():
    response = client.post("/activities/Chess Club/signup?email=student@example.com")
    assert response.status_code == 401


def test_teacher_login_allows_signup():
    login_response = client.post(
        "/login",
        json={"username": "teacher", "password": "teacher123"},
    )
    assert login_response.status_code == 200

    response = client.post(
        "/activities/Chess Club/signup?email=student@example.com",
        cookies=login_response.cookies,
    )
    assert response.status_code == 200


def test_teacher_can_unregister_student():
    login_response = client.post(
        "/login",
        json={"username": "teacher", "password": "teacher123"},
    )
    cookies = login_response.cookies

    response = client.delete(
        "/activities/Chess Club/unregister?email=student@example.com",
        cookies=cookies,
    )
    assert response.status_code == 200
