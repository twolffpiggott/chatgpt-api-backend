from typing import Optional

from pydantic import BaseModel


class ChatBase(BaseModel):
    summary: Optional[str]


class ChatCreate(ChatBase):
    pass


class ChatUpdate(ChatBase):
    pass


class Chat(ChatBase):
    id: int

    class Config:
        orm_mode = True
