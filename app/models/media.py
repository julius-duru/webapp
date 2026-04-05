from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255))
    description = Column(String(255))
    owner_id = Column(Integer, ForeignKey("users.id"))
