from fastapi import FastAPI
from app.database import Base, engine

from app.auth.routes import router as auth_router
from app.media.routes import router as media_router
from app.users.routes import router as users_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Media App")

app.include_router(auth_router)
app.include_router(media_router)
app.include_router(users_router)

@app.get("/")
def root():
    return {"message": "FastAPI Media App Running"}