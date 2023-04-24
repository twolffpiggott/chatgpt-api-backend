from pydantic import BaseModel


class LabelBase(BaseModel):
    name: str


class LabelCreate(LabelBase):
    pass


class Label(LabelBase):
    id: int
    chat_id: int

    class Config:
        orm_mode = True
