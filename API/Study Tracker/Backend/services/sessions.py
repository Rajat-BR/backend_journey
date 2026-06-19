from database.connection import get_connection
from schemas.sessions import SessionCreate, SessionUpdate

def fetch_sessions():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM sessions")
        rows = cursor.fetchall()

        if not rows:
            raise ValueError("No Session Found")
        
        return [dict(row) for row in rows]
    
    finally:
        if conn:
            conn.close()

def fetch_session_by_id(id: int):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM sessions WHERE id = ?", (id,))

        row = cursor.fetchone()
        if not row:
            raise ValueError("Session not found")
        
        return dict(row)
    
    finally:
        if conn:
            conn.close()


def new_session(session: SessionCreate):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO sessions (subject, topic, duration, notes) 
            VALUES (?, ?, ?, ?)
            """,
            (session.subject, session.topic, session.duration, session.notes))
        conn.commit()

        return {"message": f"session added successfully, last row : {cursor.lastrowid}"}
    
    finally:
        if conn:
            conn.close()

def change_session(id: int, update_data: SessionUpdate):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        update_dict = update_data.model_dump(exclude_unset=True)
        if not update_dict:
            return {"message": "Nothing to update"}
        fields=[]
        values=[]
        for key, value in update_dict.items():
            fields.append(f"{key} = ?")
            values.append(value)

        query_part = ", ".join(fields)
        values.append(id)
        cursor.execute(f"""
            UPDATE sessions
            SET {query_part}
            WHERE id = ?
                """,
            values)   

        if cursor.rowcount == 0:
            raise ValueError("Session not found")
        
        conn.commit()
        return {"message": "Session updated successfully"} 
    finally:
        if conn:
            conn.close()

def remove_session(id: int):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM sessions WHERE id = ?", (id,))

        if cursor.rowcount == 0:
            raise ValueError("Session Not Found")
        
        conn.commit()
        return {"message": "Session removed Successfully"}
    finally:
        if conn:
            conn.close()