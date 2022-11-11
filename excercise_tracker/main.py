from typing import Union
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import date

from . import schemas, models, crud
from .database import SessionLocal, engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()

@app.get("/")
def get_root():
    return "Welcome to the Excercise Tracker!"

def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)

@app.post("/api/users", response_model=schemas.User)
def create_new_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    if crud.get_db_users_by_username(db, username=user.username):
        raise_bad_request(f"Username {user.username} already used. Please use another username.")

    db_user = crud.create_new_db_user(db, user.username)
    return db_user

@app.get("/api/users", response_model=schemas.AllUser)
def get_all_user(db:Session = Depends(get_db)):
    db_users = crud.get_all_users(db)

    return schemas.AllUser(
        count=len(db_users),
        users=db_users
    )

@app.post("/api/users/{uid}/excercise", response_model=schemas.ExcerciseInfo, name="Add Excercise")
def create_excercise(excercise: schemas.ExcerciseBase, db: Session = Depends(get_db)):
    db_user = crud.get_db_users_by_uid(db, excercise.uid)
    if not db_user:
        raise_bad_request(f"Id {excercise.uid} is not registered yet. Please create a new user first")
    
    db_excercise = crud.create_db_excercise(db, excercise)
    db_excercise.username = db_user.username

    return db_excercise

@app.get("/api/users/{uid}/logs", response_model=schemas.UserInfo)
def get_excercise_log(uid: str, date_from: Union[date, None] = None, to: Union[date, None] = None, limit: Union[int, None] = None, db: Session = Depends(get_db)):
    username = crud.get_db_users_by_uid(db, uid).username

    db_excercise = crud.get_db_excercise_by_uid(db, uid, date_from, to, limit)

    excercises = [
            schemas.Excercise(description=item.description, duration=item.duration, date=item.date) for item in db_excercise
        ]

    return schemas.UserInfo(
        username=username,
        uid=uid,
        count=len(excercises),
        logs=excercises
    )