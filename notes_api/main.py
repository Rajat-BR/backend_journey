from fastapi import FastAPI, HTTPException 
from pydantic import BaseModel
from database import get_connection

app = FastAPI()

class Note(BaseModel):
    title: str
    content: str
    is_pinned: bool = False

 
@app.get("/")
def home():
    return {"message": "Notes API running"}


@app.post("/notes")
def create_note(note: Note):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO notes(title, content, is_pinned) VALUES (?, ?, ?)",
        (note.title, note.content, note.is_pinned)
    )
    
    conn.commit()
    conn.close()

    return {"message": "Note created successfully"}


@app.get("/notes")
def get_notes():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM notes")
    rows = cursor.fetchall()

    conn.close()

    notes = []
    for row in rows:
        note = dict(row)
        note["is_pinned"] = bool(note["is_pinned"])
        notes.append(note)

    return notes



@app.get("/notes/{note_id}")
def get_note(note_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
    row = cursor.fetchone()

    if cursor.rowcount is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Note not found")
    
    conn.close()
    output = dict(row)
    output["is_pinned"] = bool(output["is_pinned"])

    return output


@app.put("/notes/{note_id}")
def update_note(updated_note: Note, note_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE notes SET title = ? , content = ? , is_pinned = ? WHERE id = ?",
                   (updated_note.title, updated_note.content, updated_note.is_pinned, note_id))
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Note not found")
    
    conn.commit()
    conn.close()

    return {"message": "Note updated successfully"}


@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Note not found")
    
    conn.commit()
    conn.close()

    return {"message": "Note deleted successfully"}