from fastapi import APIRouter, HTTPException, Depends
from schemas.sessions import SessionCreate, SessionOut, SessionUpdate, SessionFilter
from services.sessions import fetch_sessions, fetch_session_by_id, new_session, change_session, remove_session
from exceptions.custom_exceptions import SessionNotFoundError, InvalidSortFieldError


router = APIRouter()

@router.get("/")
def home():
    return {"message": "API running"}

@router.get("/sessions", response_model=list[SessionOut])
def get_sessions(filters: SessionFilter = Depends(),
                 search: str | None = None,
                 sort_by: str | None = None,
                 order: str = "asc",
                 page: int = 1,
                 limit: int = 50):
    try:
        return fetch_sessions(filters, search, sort_by, order, page, limit)
    except SessionNotFoundError:
        raise HTTPException(status_code=404, detail="No Sessions found")
    except InvalidSortFieldError:
        raise HTTPException(status_code=400, detail="Bad Request")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/sessions/{id}", response_model=SessionOut)
def get_session_by_id(id: int):
    try:
        return fetch_session_by_id(id)
    except SessionNotFoundError:
        raise HTTPException(status_code=404, detail="Session Not Found")
    except InvalidSortFieldError:
        raise HTTPException(status_code=400, detail="Bad request")
    
@router.post("/sessions")
def create_session(session: SessionCreate):
    return new_session(session)

@router.patch("/sessions/{id}")
def update_session(id: int, update_data: SessionUpdate):
    try:
        return change_session(id, update_data)
    except SessionNotFoundError:
        raise HTTPException(status_code=404, detail="Session Not found")
    
@router.delete("/sessions/{id}")
def delete_session(id: int):
    try:
        return remove_session(id)
    except SessionNotFoundError:
        raise HTTPException(status_code=404, detail="Session Not Found")