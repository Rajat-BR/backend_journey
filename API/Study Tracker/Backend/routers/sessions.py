from fastapi import APIRouter, HTTPException
from schemas.sessions import SessionCreate, SessionOut, SessionUpdate
from services.sessions import fetch_sessions, fetch_session_by_id, new_session, change_session, remove_session

router = APIRouter()

@router.get("/")
def home():
    return {"message": "API running"}

@router.get("/sessions", response_model=list[SessionOut])
def get_sessions(search: str | None = None):
    try:
        return fetch_sessions(search)
    except ValueError:
        raise HTTPException(status_code=404, detail="No Sessions found")
    
@router.get("/sessions/{id}", response_model=SessionOut)
def get_session_by_id(id: int):
    try:
        return fetch_session_by_id(id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Session Not Found")
    
@router.post("/sessions")
def create_session(session: SessionCreate):
    return new_session(session)

@router.patch("/sessions/{id}")
def update_session(id: int, update_data: SessionUpdate):
    try:
        return change_session(id, update_data)
    except ValueError:
        raise HTTPException(status_code=404, detail="Session Not found")
    
@router.delete("/sessions/{id}")
def delete_session(id: int):
    try:
        return remove_session(id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Session Not Found")