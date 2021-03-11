import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from sqlalchemy.orm import Session
from models import *
import bcrypt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def seed_ruangan(db: Session):
    if db is None:
        db = SessionLocal()
    df = pd.read_csv('seed/Ruangan.csv')
    df = df.astype(object)
    try:
        for i in range(0, df.shape[0]):
            ruangan = Ruangan(id=df.iloc[i]['KdRuangan'],
                      nama=df.iloc[i]['NamaRuangan'],
                      id_instalasi=df.iloc[i]['KdInstalasi']
                     )
            db.add(ruangan)
            db.commit()
            db.refresh(ruangan)
    except Exception:
        db.rollback()
    del df

def reset_ruangan(db: Session):
    try:
        db.query(Ruangan).delete()
        db.commit()
    except Exception:
        db.rollback()

def get_ruangan(db: Session):
    try:
        ruangan = db.query(Ruangan).all()
        return ruangan
    except Exception:
        db.rollback()

def get_ruangan_by_id(db: Session, id: str):
    try:
        ruangan = db.query(Ruangan).filter(Ruangan.id == id).first()
        return ruangan
    except Exception:
        db.rollback()
