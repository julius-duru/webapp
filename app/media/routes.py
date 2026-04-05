from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.media import Media
from app.auth.dependencies import get_current_user
from app.media.utils import save_file

router = APIRouter(prefix="/media", tags=["Media"])

# CREATE (Upload)
@router.post("/upload")
def upload_file(
    description: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    filename = save_file(file)

    media = Media(
        filename=filename,
        description=description,
        owner_id=user.id
    )

    db.add(media)
    db.commit()

    return {"message": "Uploaded successfully"}

# READ
@router.get("/")
def get_media(db: Session = Depends(get_db)):
    return db.query(Media).all()

# UPDATE
@router.put("/{media_id}")
def update_media(
    media_id: int,
    description: str,
    db: Session = Depends(get_db)
):
    media = db.query(Media).get(media_id)
    media.description = description
    db.commit()

    return {"message": "Updated"}

# DELETE
@router.delete("/{media_id}")
def delete_media(media_id: int, db: Session = Depends(get_db)):
    media = db.query(Media).get(media_id)
    db.delete(media)
    db.commit()

    return {"message": "Deleted"}