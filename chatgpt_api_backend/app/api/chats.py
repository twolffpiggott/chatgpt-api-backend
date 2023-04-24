from typing import List

from app.database import models, session
from app.schemas import chat as chat_schema
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", response_model=chat_schema.Chat)
def create_chat(chat: chat_schema.ChatCreate, db: Session = Depends(session.get_db)):
    new_chat = models.Chat(summary=chat.summary)
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    return new_chat


@router.get("/", response_model=List[chat_schema.Chat])
def read_chats(skip: int = 0, limit: int = 100, db: Session = Depends(session.get_db)):
    chats = db.query(models.Chat).offset(skip).limit(limit).all()
    return chats


@router.get("/{chat_id}", response_model=chat_schema.Chat)
def read_chat(chat_id: int, db: Session = Depends(session.get_db)):
    chat = db.query(models.Chat).filter(models.Chat.id == chat_id).first()
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat


@router.put("/{chat_id}", response_model=chat_schema.Chat)
def update_chat(
    chat_id: int, chat: chat_schema.ChatUpdate, db: Session = Depends(session.get_db)
):
    db_chat = db.query(models.Chat).filter(models.Chat.id == chat_id).first()
    if db_chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")

    if chat.summary:
        db_chat.summary = chat.summary

    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat


@router.delete("/{chat_id}", response_model=chat_schema.Chat)
def delete_chat(chat_id: int, db: Session = Depends(session.get_db)):
    chat = db.query(models.Chat).filter(models.Chat.id == chat_id).first()
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")

    db.delete(chat)
    db.commit()
    return chat
