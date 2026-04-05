from passlib.context import CryptContext
from jose import jwt

SECRET_KEY = "secret"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(root):
    return pwd_context.hash(root)

def verify_password(root, hashed):
    return pwd_context.verify(root, hashed)

def create_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)