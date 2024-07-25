from fastapi import FastAPI, BackgroundTasks, HTTPException, Depends, Response, File, UploadFile, Request
from sqlalchemy.orm import Session
import os
import asyncio
from uuid import uuid4
import schemas, models, database,crud
from email_utils import send_email
from jose import JWTError
from config import SECRET_KEY
import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models import Child
from crud import get_password_hash
from typing import List, Optional,Dict, Any

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register/", response_model=schemas.Parent)
def register_parent(parent: schemas.ParentCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    email = parent.email
    parent.password = get_password_hash(parent.password)
    first_name = parent.first_name
    last_name= parent.last_name
    db_parent = db.query(models.Parent).filter(models.Parent.email == email).first()
    if db_parent:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    payload = {
        'username': email,
        'exp': datetime.now() + timedelta(hours=1)  # Token expiration time
    }



    # Generate the JWT token
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    new_parent = models.Parent(
        first_name=parent.first_name,
        last_name=parent.last_name,
        age=parent.age,
        address=parent.address,
        city=parent.city,
        country=parent.country,
        pincode=parent.pincode,
        email=parent.email,
        hashed_password=parent.password,
        activation_token=token,
        profile_photo=parent.profile_photo
    )
    
    db.add(new_parent)
    db.commit()
    db.refresh(new_parent)
    
    activation_link = f"http://localhost:8000/activate/{new_parent.activation_token}/"
    subject="Activate Your Account"
    body = f"""
    Dear {parent.first_name},

    Please click on the following link to activate your account:
    {activation_link}

    Best regards,
    Your Application Team
    """
    background_tasks.add_task(send_email, new_parent.email,subject, body)
    
    return Response(content='success', status_code=200)



@app.post("/activate/{activation_token}/", response_model=schemas.Parent)
def activate_parent(activation_token: str, db: Session = Depends(get_db)):
    parent = db.query(models.Parent).filter(models.Parent.activation_token == activation_token).first()
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    
    parent.is_active = True
    parent.activation_token = None
    db.commit()

    return Response(content='your account activated', status_code=200)

@app.post("/login/")
def login_parent(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    email = form_data.username
    password = form_data.password
    parent = crud.get_parent_by_email(db, email)
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    if not crud.verify_password(password, parent.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    # Generate JWT token
    access_token_expires = timedelta(hours=1)
    access_token = crud.create_access_token(data={"sub": parent.email}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}



UPLOAD_DIRECTORY = "uploads/profile_pictures/"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

async def parse_form_data(request: Request) -> Dict[str, Any]:
    form = await request.form()
    form_dict = {key: value for key, value in form.items()}
    return form_dict


@app.put("/parent/profile/{parent_id}", response_model=schemas.Parent)
def update_parent_profile(
    parent_id: int,
    profile_update: Dict[str, Any] = Depends(parse_form_data),
    profile_photo: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    parent = db.query(models.Parent).filter(models.Parent.id == parent_id).first()

    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    
    
    if "first_name" in profile_update:
        parent.first_name = profile_update["first_name"]
    if "last_name" in profile_update:
        parent.last_name = profile_update["last_name"]
    if "age" in profile_update:
        parent.age = profile_update["age"]
    if "address" in profile_update:
        parent.address = profile_update["address"]
    if "city" in profile_update:
        parent.city = profile_update["city"]
    if "country" in profile_update:
        parent.country = profile_update["country"]
    if "pincode" in profile_update:
        parent.pincode = profile_update["pincode"]
    if "email" in profile_update:
        parent.email = profile_update["email"]

    if profile_photo:
        file_extension = os.path.splitext(profile_photo.filename)[1]
        profile_photo_filename = f"{uuid4()}{file_extension}"

        # Save the uploaded file
        file_path = os.path.join(UPLOAD_DIRECTORY, profile_photo_filename)
        with open(file_path, "wb") as buffer:
            buffer.write(profile_photo.file.read())

        # Update the profile photo path in the database
        parent.profile_photo = file_path

   
    
    # # Commit the changes to the database
    db.commit()
    db.refresh(parent)

    return parent



@app.post("/parents/{parent_id}/children/", response_model=schemas.Child)
def create_child_for_parent(
    parent_id: int, child: schemas.ChildCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)
):
    db_parent = crud.get_parent(db, parent_id)
    if not db_parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    
    
    db_child = crud.create_child(db=db, child=child, parent_id=parent_id)
    print(f'Created child: {db_child}')
    subject="Child creation"
    body=f"""
    Dear {db_parent.first_name},

    we have successfully added {child.name} as child in your account:

    Best regards,
    Your Application Team
    """
    background_tasks.add_task(send_notification,db_parent.email,subject, body)
    return db_child

def send_notification(email,subject, body):
    import time
    time.sleep(30)
    send_email(email,subject, body)

@app.get("/parents/{parent_id}/children/", response_model=List[schemas.Child])
def read_children(
    parent_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    children = crud.get_children(db, parent_id=parent_id, skip=skip, limit=limit)
    return children

@app.put("/children/{child_id}/", response_model=schemas.Child)
def update_child(child_id: int, child: schemas.ChildCreate, db: Session = Depends(get_db)):
    db_child = db.query(Child).filter(Child.child_id == child_id).first()
    if db_child is None:
        raise HTTPException(status_code=404, detail="Child not found")
    
    # Update only the fields provided in the request
    update_data = child.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_child, key, value)
    
    db.commit()
    db.refresh(db_child)
    return db_child

@app.get("/children/", response_model=List[schemas.Child])
def list_children(
    parent_id: int, 
    added_after: Optional[datetime] = None,
    name_contains: Optional[str] = None,
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db)
):
    filters = []
    
    # Filter by parent_id
    filters.append(models.Child.parent_id == parent_id)
    
    # Filter by date of addition (added_after)
    if added_after:
        filters.append(models.Child.date_added >= added_after)
    
    # Filter by name contains (name_contains)
    if name_contains:
        filters.append(models.Child.name.contains(name_contains))
    
    # Query children with applied filters
    query = db.query(models.Child).filter(*filters).offset(skip).limit(limit)
    children = query.all()
    
    return children


