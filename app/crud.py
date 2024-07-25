from sqlalchemy.orm import Session
import models, schemas
from datetime import datetime, timedelta
from jose import JWTError
import jwt
from passlib.context import CryptContext
import secrets
from models import Child, Parent
from schemas import ChildCreate

SECRET_KEY = secrets.token_hex(32) 
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)

def get_parent_by_email(db: Session, email: str):
    return db.query(models.Parent).filter(models.Parent.email == email).first()

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def update_parent_profile(db: Session, parent_id: int, profile_update: schemas.Parent):
    db_parent = db.query(models.Parent).filter(models.Parent.id == parent_id).first()
    if not db_parent:
        return None
    
    for field, value in profile_update.dict(exclude_unset=True).items():
        setattr(db_parent, field, value)


def get_child(db: Session, child_id: int):
    return db.query(Child).filter(Child.id == child_id).first()

def get_children(db: Session, parent_id: int = None, skip: int = 0, limit: int = 10):
    query = db.query(Child)
    if parent_id:
        query = query.filter(Child.parent_id == parent_id)
    return query.offset(skip).limit(limit).all()

def create_child(db: Session, child: ChildCreate, parent_id: int):
    db_child = Child(**child.model_dump(), parent_id=parent_id)
    db.add(db_child)
    db.commit()
    db.refresh(db_child)
    return db_child

def get_parent(db: Session, parent_id: int):
    return db.query(models.Parent).filter(models.Parent.id == parent_id).first()

def update_child(db: Session, child_id: int, child: ChildCreate):
    db_child = db.query(Child).filter(Child.id == child_id).first()
    if db_child:
        db_child.name = child.name
        db.commit()
        db.refresh(db_child)
    return db_child

