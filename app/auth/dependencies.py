from fastapi import Depends, HTTPException
from jose import jwt
from app.database import get_db
from sqlalchemy.orm import Session
from app.models.user import User

SECRET_KEY = "secret"
ALGORITHM = "HS256"

def get_current_user(token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = db.query(User).get(payload["user_id"])
        return user
    except:
        raise HTTPException(status_code=401, detail="Unauthorized")