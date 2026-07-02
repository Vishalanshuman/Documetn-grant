
from pydantic import BaseModel
from uuid import UUID


class DocumentBase(BaseModel):
    name: str


class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(DocumentBase):
    pass

class Document(DocumentBase):
    id: UUID

    class Config:
        orm_mode = True
