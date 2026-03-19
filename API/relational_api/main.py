from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import get_connection

app = FastAPI()

class Task(BaseModel):
    title: str
    completed: bool = False
    user_id: int

class TaskOut(BaseModel):
    id: int
    title: str
    completed: bool

class UserTaskResponse(BaseModel):
    username: str
    tasks: list[TaskOut]


def format_row(row):
    task= dict(row)
    task["completed"]= bool(task["completed"])
    return task


@app.get("/")
def home():
    return {"message": "Reltaional API running"}


@app.post("/tasks")
def create_task(task: Task):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO tasks(title, completed, user_id) VALUES(?, ?, ?)",
                   (task.title, task.completed, task.user_id))
    
    conn.commit()
    conn.close()

    return {"message": "Task created successfully"}


@app.get("/tasks", response_model=UserTaskResponse)
def get_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    
    conn.close()

    tasks = [format_row(row) for row in rows]

    return tasks


@app.get("/users/{user_id}/tasks-join", response_model=UserTaskResponse)
def get_user_tasks_join(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user= cursor.fetchone()

    if user is None:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    
    username = user["username"]

    cursor.execute("""SELECT users.username, tasks.id, tasks.title, tasks.completed 
                   FROM users 
                   JOIN tasks 
                   ON tasks.user_id = users.id 
                   WHERE users.id = ?""",
                   (user_id,))
    
    rows = cursor.fetchall()
    conn.close()

    tasks= []
    for row in rows:
        task= {
            "id": row["id"],
            "title": row["title"],
            "completed": bool(row["completed"])
        }
        tasks.append(task)
    
    return {
        "username": username,
        "tasks": tasks 
    }


@app.get("/users/{user_id}/tasks-left-join", response_model=UserTaskResponse)
def get_user_tasks_left_join(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT users.username, tasks.id, tasks.title, tasks.completed 
        FROM users
        LEFT JOIN tasks
        ON tasks.user_id = users.id
        WHERE users.id = ?
        """,
        (user_id,))
    
    rows = cursor.fetchall()

    if not rows:
        conn.close()
        raise HTTPException(status_code=404, detail="User Not found")
    
    username = rows[0]["username"]

    tasks = []
    for row in rows:
        if row["id"] is None:
            continue

        task = {
            "id": row["id"],
            "title": row["title"],
            "completed": bool(row["completed"])
        }
        tasks.append(task)

    conn.close()

    return {
        "username": username,
        "tasks": tasks
    }

