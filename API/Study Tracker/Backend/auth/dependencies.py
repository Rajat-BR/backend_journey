from fastapi import HTTPException, Depends
from database.connection import get_connection
from auth.security import decode_access_token, oauth2_scheme
from exceptions.custom_exceptions import InvalidTokenError
from schemas.sessions import UserOut

def get_current_user(token: str=Depends(oauth2_scheme)):
    conn = None
    try:
        payload = decode_access_token(token)

        user_id = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()

        if not row:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        
        return UserOut(
            id=row["id"],
            username=row["username"]
        ) 
    
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    finally:
        if conn:
            conn.close()    
