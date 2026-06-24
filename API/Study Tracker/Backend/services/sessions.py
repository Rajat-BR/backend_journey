from database.connection import get_connection
from schemas.sessions import SessionCreate, SessionUpdate, UserLogin, UserRegister, UserOut
from exceptions.custom_exceptions import SessionNotFoundError, InvalidSortFieldError, UserAlreadyExistsError
from auth.security import hash_password, verify_password

def fetch_sessions(filters, search, sort_by, order, page, limit):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        conditions = []
        values = []
        allowed_sort = {"id", "subject", "topic", "duration", "notes"}
        allowed_order = {"asc","desc"}
        order = order.lower()
        filter_dict = filters.model_dump(exclude_none=True)

        if filter_dict:
            for key, value in filter_dict.items():
                conditions.append(f"{key} = ?")
                values.append(value)
        
        if search:
                search_text = f"%{search}%"
                conditions.append("(subject LIKE ? OR topic LIKE ? OR notes LIKE ?)")
                values.extend([search_text]*3)
        
        query = "SELECT * FROM sessions"
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        if sort_by:
            if sort_by not in allowed_sort:
                raise InvalidSortFieldError()
            
            if order not in allowed_order:
                order = "asc"

            query += f" ORDER BY {sort_by} {order.upper()}"

        
        if page < 1:
            raise ValueError("Invalid page")
        if limit < 1:
            raise ValueError("Invalid Limit")
        
        offset = (page - 1) * limit

        query += " LIMIT ? OFFSET ?"
        values.extend([limit, offset])

        
        cursor.execute(query, values)
        
        rows = cursor.fetchall()
        if not rows:
            return []
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
            raise SessionNotFoundError()
        
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
            raise SessionNotFoundError()
        
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
            raise SessionNotFoundError()
        
        conn.commit()
        return {"message": "Session removed Successfully"}
    finally:
        if conn:
            conn.close()


def register_user(user: UserRegister):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM users WHERE username = ?", (user.username,)) #Only care whether the username exists or not. Why select everything ?
        row = cursor.fetchone()

        if row:
            raise UserAlreadyExistsError("Username already exists !")
        
        hashed_password = hash_password(user.password)

        cursor.execute("INSERT INTO users(username,hashed_password) VALUES (?, ?)", (user.username, hashed_password))

        user_id = cursor.lastrowid
        
        conn.commit()

        return UserOut(
            id=user_id,
            username=user.username
        )

    finally:
        if conn:
            conn.close()