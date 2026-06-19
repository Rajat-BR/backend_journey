from pydantic import BaseModel

class SessionCreate(BaseModel):
    subject: str
    topic: str
    duration: int
    notes: str

class SessionOut(BaseModel):
    id: int
    subject: str
    topic: str
    duration: int
    notes: str

class SessionUpdate(BaseModel):
    subject: str | None = None
    topic: str | None = None
    duration: int | None = None
    notes: str | None = None