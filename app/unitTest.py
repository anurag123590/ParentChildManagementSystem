import pytest
from httpx import HTTPStatusError
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from main import app, get_db
import models, schemas
from config import SECRET_KEY

# SQLAlchemy setup
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:12345678@localhost/admin_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency override for FastAPI application
def override_get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# Pytest fixtures
@pytest.fixture(scope="module")
def client():
    with TestClient(app=app) as c:
        yield c

@pytest.fixture(scope="function")
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Test function
def test_register_parent(client, db):
    parent_data = {
        "first_name": "Raj",
        "last_name": "Doe",
        "age": 35,
        "address": "123 Main St",
        "city": "Anytown",
        "country": "USA",
        "pincode": "12345",
        "email": "nomadmodeon@gmail.com",
        "password": "password123"
    }

    try:
        response = client.post("/register/", json=parent_data)
        response.raise_for_status()  # Raise an error for non-2xx responses
    except HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
        assert e.response.status_code == 200  # Adjust as necessary based on expected behavior
    except Exception as e:
        print(f"Request error: {e}")
        assert False, f"Unexpected exception occurred: {e}"

    db_parent = db.query(models.Parent).filter(models.Parent.email == parent_data["email"]).first()
    assert db_parent is not None
    assert db_parent.email == parent_data["email"]


def test_activate_parent(client, db):
    # Initial setup: Ensure parent exists
    parent = db.query(models.Parent).filter(models.Parent.email == "nomadmodeon@gmail.com").first()
    assert parent is not None, "Parent should exist in the database before activation"
    activation_token = parent.activation_token    
    # Make the activation request
    response = client.post(f"/activate/{activation_token}/")
    print(f"Response: status_code={response.status_code}, content={response.content.decode()}")
    assert response.status_code == 200
    assert response.content.decode() == 'your account activated'
    # Refresh the parent instance
    db.refresh(parent)
    
    # Fetch the parent instance again
    db_parent = db.query(models.Parent).filter(models.Parent.email == "nomadmodeon@gmail.com").first()
    
    # Final state logging    
    # Assert the final state
    assert db_parent.is_active is True
    assert db_parent.activation_token is None


def test_login_parent(client):
    login_data = {
        "username": "nomadmodeon@gmail.com",
        "password": "password123"
    }

    response = client.post("/login/", data=login_data)
    assert response.status_code == 200
    json_response = response.json()
    assert "access_token" in json_response
    assert json_response["token_type"] == "bearer"


def test_update_parent_profile(client, db):
    parent = db.query(models.Parent).filter(models.Parent.email == "nomadmodeon@gmail.com").first()

    profile_update = {
        "first_name": "Jane",
        "last_name": "Doe",
        "age": 30,
        "address": "456 Elm St",
        "city": "Othertown",
        "country": "Canada",
        "pincode": "67890"
    }

    with open("test_photo.jpg", "rb") as file:
        files = {"profile_photo": ("test_photo.jpg", file, "image/jpeg")}
        response = client.put(f"/parent/profile/{parent.id}", data=profile_update, files=files)

    assert response.status_code == 200
    updated_parent = response.json()
    assert updated_parent["first_name"] == "Jane"
    assert updated_parent["last_name"] == "Doe"


def test_create_child_for_parent(client, db):
    parent = db.query(models.Parent).filter(models.Parent.email == "nomadmodeon@gmail.com").first()
    child_data = {
        "name": "Little John",
        "age": 5,
        "date_of_birth": "2019-01-01"
    }

    response = client.post(f"/parents/{parent.id}/children/", json=child_data)
    assert response.status_code == 200
    created_child = response.json()
    assert created_child["name"] == "Little John"


def test_read_children(client, db):
    parent = db.query(models.Parent).filter(models.Parent.email == "nomadmodeon@gmail.com").first()

    response = client.get(f"/parents/{parent.id}/children/")
    assert response.status_code == 200
    children = response.json()
    assert isinstance(children, list)


def test_update_child(client, db):
    child = db.query(models.Child).filter(models.Child.name == "Little John").first()
    child_update = {
        "name": "Little Jane",
        "age": 6
    }

    response = client.put(f"/children/{child.child_id}/", json=child_update)
    assert response.status_code == 200
    updated_child = response.json()
    assert updated_child["name"] == "Little Jane"


def test_list_children(client, db):
    parent = db.query(models.Parent).filter(models.Parent.email == "nomadmodeon@gmail.com").first()

    response = client.get(f"/children/?parent_id={parent.id}")
    assert response.status_code == 200
    children = response.json()
    assert isinstance(children, list)
