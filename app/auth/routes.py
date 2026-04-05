from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.auth.utils import hash_password, verify_password, create_token

router = APIRouter(prefix="/auth", tags=["Auth"])

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.auth.utils import hash_password

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # 🔍 Check if user already exists
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        # 🔐 Enforce bcrypt-safe password length (bytes, not characters)
        password_bytes = user.password.encode("utf-8")
        if len(password_bytes) > 72:
            raise HTTPException(
                status_code=400,
                detail="Password too long (max 72 bytes for bcrypt)"
            )

        # 🔑 Hash password safely
        hashed_password = hash_password(user.password)

        # 💾 Save user
        new_user = User(
            email=user.email,
            password=hashed_password
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"message": "User created successfully"}

    except HTTPException:
        raise

    except SQLAlchemyError as e:
        db.rollback()
        print("DB ERROR:", str(e))
        raise HTTPException(status_code=500, detail="Database error")

    except Exception as e:
        print("GENERAL ERROR:", str(e))
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"user_id": db_user.id})
    return {"access_token": token, "token_type": "bearer"}