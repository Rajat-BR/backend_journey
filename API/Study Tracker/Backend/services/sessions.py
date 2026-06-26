from fastapi import Depends
from database.connection import get_connection
from schemas.sessions import SessionCreate, SessionUpdate, UserLogin, UserRegister, UserOut, Token
from exceptions.custom_exceptions import SessionNotFoundError, InvalidSortFieldError, UserAlreadyExistsError, InvalidCredentialsError
from auth.security import hash_password, verify_password, create_access_token, oauth2_scheme, decode_access_token

def fetch_sessions(user_id, filters, search, sort_by, order, page, limit):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        conditions = []
        values = []
        values.append(user_id)
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
        
        query = "SELECT * FROM sessions WHERE user_id = ?"
        if conditions:
            query += " AND " + " AND ".join(conditions)

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

def fetch_session_by_id(id: int, user_id: int):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM sessions WHERE id = ? AND user_id = ?", (id, user_id))

        row = cursor.fetchone()
        if not row:
            raise SessionNotFoundError()
        
        return dict(row)
    
    finally:
        if conn:
            conn.close()


def new_session(session: SessionCreate, user_id):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO sessions (subject, topic, duration, notes, user_id) 
            VALUES (?, ?, ?, ?, ?)
            """,
            (session.subject, session.topic, session.duration, session.notes, user_id))
        conn.commit()

        return {"message": f"session added successfully, last row : {cursor.lastrowid}"}
    
    finally:
        if conn:
            conn.close()

def change_session(id: int, update_data: SessionUpdate, user_id):
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
        values.extend([id, user_id])
        cursor.execute(f"""
            UPDATE sessions
            SET {query_part}
            WHERE id = ?
            AND user_id = ?
                """,
            values)   

        if cursor.rowcount == 0:
            raise SessionNotFoundError()
        
        conn.commit()
        return {"message": "Session updated successfully"} 
    finally:
        if conn:
            conn.close()

def remove_session(id: int, user_id):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM sessions WHERE id = ? AND user_id = ?", (id,user_id))

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
        
        # Check if the user exists
        cursor.execute("SELECT id FROM users WHERE username = ?", (user.username,)) #Only care whether the username exists or not. Why select everything ?
        row = cursor.fetchone()

        if row:
            raise UserAlreadyExistsError("Username already exists !")
        
        # Else
        hashed_password = hash_password(user.password)

        cursor.execute("INSERT INTO users(username,hashed_password) VALUES (?, ?)", (user.username, hashed_password))

        conn.commit()

        user_id = cursor.lastrowid
        
        return UserOut(
            id=user_id,
            username=user.username
        )

    finally:
        if conn:
            conn.close()

def login_user(form_data):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Check if the user exists
        cursor.execute("SELECT id, hashed_password FROM users WHERE username = ?", (form_data.username,))
        rows = cursor.fetchone()

        if not rows:
            raise InvalidCredentialsError("Invalid Credential")
        
        user_id = rows["id"]
        hashed_password = rows["hashed_password"]

        if not verify_password(form_data.password, hashed_password):
            raise InvalidCredentialsError("Invalid Credentials")
        
        token = create_access_token(
            {"sub": str(user_id)}    #user_id is an integer, so convert it to dicitionary
        )
        
        return Token(
            access_token=token,
            token_type="bearer"
        )

    finally:
        if conn:
            conn.close()  
    
