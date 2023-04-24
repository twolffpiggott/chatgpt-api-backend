from app.database.base import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    summary = Column(String)

    messages = relationship("Message", back_populates="chat")
    labels = relationship("Label", back_populates="chat")


class MessageType(Base):
    __tablename__ = "message_types"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, unique=True)

    messages = relationship("Message", back_populates="message_type")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    content = Column(String)
    message_type_id = Column(Integer, ForeignKey("message_types.id"))
    timestamp = Column(DateTime)

    chat = relationship("Chat", back_populates="messages")
    message_type = relationship("MessageType", back_populates="messages")
    embedding = relationship("Embedding", uselist=False, back_populates="message")

    __table_args__ = (
        UniqueConstraint("chat_id", "timestamp", name="unique_chat_timestamp"),
    )


class Embedding(Base):
    __tablename__ = "embeddings"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("messages.id"), unique=True)
    vector = Column(String)

    message = relationship("Message", back_populates="embedding")


class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    chat_id = Column(Integer, ForeignKey("chats.id"))

    chat = relationship("Chat", back_populates="labels")
