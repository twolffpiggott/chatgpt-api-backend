from app.database import models, session
from app.schemas import label as label_schema
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", response_model=label_schema.Label)
def create_label(
    chat_id: int, label: label_schema.LabelCreate, db: Session = Depends(session.get_db)
):
    chat = db.query(models.Chat).filter(models.Chat.id == chat_id).first()
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")

    new_label = models.Label(name=label.name, chat_id=chat_id)
    db.add(new_label)
    db.commit()
    db.refresh(new_label)
    return new_label


@router.delete("/{label_id}", response_model=label_schema.Label)
def delete_label(label_id: int, db: Session = Depends(session.get_db)):
    label = db.query(models.Label).filter(models.Label.id == label_id).first()
    if label is None:
        raise HTTPException(status_code=404, detail="Label not found")

    db.delete(label)
    db.commit()
    return label
