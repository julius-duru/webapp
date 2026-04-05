from pydantic import BaseModel

class MediaCreate(BaseModel):
    description: str
    