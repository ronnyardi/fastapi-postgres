from typing import List
from uuid import UUID
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    try:
        yield SessionLocal()
    finally:
        SessionLocal().close()

@app.get("/")
def healthcheck():
    return {"ready": "OK"}

@app.get("/multiply", description="Insert 2 number you want to multiply")
def multiply(a: int, b: int):
    return {"status": "OK", "result": a*b}

@app.get("/users", response_model=List[schemas.User])
async def fetch_users(limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(models.User).limit(10).all()
    return users

@app.post("/users", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    else:
        fake_hashed_password = user.password + "funnyhash"
        db_user = models.User(name= user.name, email=user.email, address= user.address, hashed_password=fake_hashed_password)
        db.add(db_user)
        db.commit()
    return db_user

@app.delete("/users/{user_id}")
async def delete_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.uuid == user_id).first()
    if user:
        db.query(models.User).filter(models.User.uuid == user_id).delete()
        db.commit()
    else:
        raise HTTPException(
            status_code=404,
            detail=f"user with id {user_id} does not exist"
        )
    return {"status": "OK","message": f"user {user_id} deleted"}

@app.get("/users/{user_id}")
async def read_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.uuid == user_id).first()
    if user:
        return user
    else:
        raise HTTPException(
            status_code=404,
            detail=f"user with id {user_id} does not exist"         
        )

@app.put("/users/{user_id}")
async def update_user(user_id: str, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    user_update = db.query(models.User).filter(models.User.uuid == user_id).first()
    if user_update:
        user_update.name = user.name
        user_update.email = user.email
        user_update.address = user.address
        user_update.is_active = user.is_active
        db.add(user_update)
        db.commit()
        db.refresh(user_update)
    else:
        raise HTTPException(
            status_code=404,
            detail=f"user with id {user_id} does not exist"
        )
    return user_update