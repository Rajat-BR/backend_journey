from pydantic import BaseModel

class Session(BaseModel):
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