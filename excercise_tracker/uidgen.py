import secrets
import string
from sqlalchemy.orm import Session

from . import crud

def create_random_uid(length: int = 5) -> str:
    chars = string.ascii_lowercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))

def create_unique_random_uid(db: Session) -> str:
    uid = create_random_uid()
    while crud.get_db_users_by_uid(db, uid):
        uid = create_random_uid()
    return uid