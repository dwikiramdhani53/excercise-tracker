from sqlalchemy.orm import Session
from typing import Union
from datetime import date

from . import uidgen, models, schemas

def create_new_db_user(db: Session, username: str) -> models.User:
    uid = uidgen.create_unique_random_uid(db)

    db_user = models.User(uid=uid, username=username)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    db_user.uid = uid

    return db_user

def create_db_excercise(db: Session, excercise: schemas.ExcerciseBase):
    db_excercise = models.Excercise(uid=excercise.uid, description=excercise.description, duration=excercise.duration, date=excercise.date)

    db.add(db_excercise)
    db.commit()
    db.refresh(db_excercise)

    return db_excercise
    
def get_all_users(db: Session) -> models.User:
    return (
        db.query(models.User).all()
    )

def get_db_users_by_uid(db: Session, uid: str) -> models.User:
    return (
        db.query(models.User)
        .filter(models.User.uid == uid)
        .first()
    )

def get_db_users_by_username(db: Session, username: str) -> models.User:
    return (
        db.query(models.User)
        .filter(models.User.username == username)
        .first()
    )

def get_db_excercise_by_uid(db: Session, uid: str, date_from: Union[date, None] = None, to: Union[date, None] = None, limit: Union[int, None] = None) -> models.Excercise:
    if date_from != None and to != None:
        db_excercise = db.query(models.Excercise).filter(models.Excercise.uid == uid).filter(models.Excercise.date.between(date_from, to)).all()
    elif date_from == None and to == None:
        db_excercise = db.query(models.Excercise).filter(models.Excercise.uid == uid).filter(models.Excercise.uid == uid).all()
    elif date_from != None:
        db_excercise = db.query(models.Excercise).filter(models.Excercise.uid == uid).filter(models.Excercise.date >= date_from).all()
    else:
        db_excercise = db.query(models.Excercise).filter(models.Excercise.uid == uid).filter(models.Excercise.date <= to).all()
        

    try:
        return db_excercise[:limit]
    except:
        return db_excercise