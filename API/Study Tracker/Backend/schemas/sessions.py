from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

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

class SessionFilter(BaseModel):
    subject: str | None = None
    topic: str | None = None
    notes: str | None = None

