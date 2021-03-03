import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from sqlalchemy.orm import Session
import models
import schemas.user_scheme  as schema
import bcrypt
from datetime import datetime, timedelta


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(
        models.User.username == username,
        models.User.deleted_at == None).first()


def get_user_by_id(db: Session, id: int):
    return db.query(models.User).filter(
        models.User.id == id,
        models.User.deleted_at == None,).first()


def create_user(db: Session, user: schema.UserRegister):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = models.User(username=user.username,
                          password=hashed_password.decode('utf-8'),
                          # password=hashed_password, # for instead of postgresql
                          id_pegawai=user.id_pegawai,
                          email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def check_username_password(db: Session, user: schema.UserLogin):
    db_user_info: models.User = get_user_by_username(db, username=user.username)
    # print(db_user_info.password.decode('utf-8'))
    return bcrypt.checkpw(user.password.encode('utf-8'), db_user_info.password.encode('utf-8'))





import jwt

secret_key = "0943lds0o98icjo34kr39fucvoi3n4lkjrf09sd8iocjvl3k4t0f98dusj3kl"
algorithm = "HS256"


def create_access_token(*, data:dict, db: Session, expires_delta: timedelta=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    db_user = get_user_by_username(db=db, username=str)
    db_user.token = encoded_jwt
    db.commit()
    db.refresh(db_user)
    return encoded_jwt

def is_token(db: Session, username: str, token: str):
    db_user = get_user_by_username(db=db, username=username)
    if db_user.token == token:
        return db_user
    else:
        return None


def decode_access_token(*, data: str):
    global secret_key, algorithm
    to_decode = data
    return jwt.decode(to_decode, secret_key, algorithms=algorithm)

def create_permanent_access_token(*, data: dict, db: Session):
    global secret_key
    encoded_jwt = jwt.encode(data, secret_key, algorithm=algorithm)
    db_user = get_user_by_username(db=db, username=data["sub"])
    db_user.token = encoded_jwt
    db.commit()
    db.refresh(db_user)
    return encoded_jwt


def check_token(db: Session, username: str, token: str):
    db_user: models.User = get_user_by_username(db, username=username)
    if db_user.token == token:
        return True
    else:
        return False
