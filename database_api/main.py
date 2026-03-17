from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import get_connection

app = FastAPI()


class Task(BaseModel):
    title: str
    completed: bool = False
    user_id: int


@app.get("/")
def home():
    return {"message": "Database API running"}


@app.post("/tasks")
def create_task(task: Task):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks (title, completed, user_id) VALUES(?, ?, ?)",
        (task.title, task.completed, task.user_id)
    )

    conn.commit()
    conn.close()

    return {"message": "Task created successfully"}


@app.get("/tasks")
def get_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()

    conn.close()

    tasks = []
    for row in rows:
        task = dict(row)
        task["completed"] = bool(task["completed"])
        tasks.append(task)

    return tasks


@app.get("/tasks/{user_id}")
def get_tasks_by_user_id(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE user_id = ? ", (user_id,))
    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


@app.get("/task/{task_id}")
def get_task(task_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()

    conn.close()

    if row is None:
        raise HTTPException(status_code = 404, detail = "Task not found")

    output = dict(row)
    output["completed"] = bool(output["completed"])
    
    return output


@app.put("/tasks/{task_id}")
def put_task(updated_task: Task, task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET title = ? , completed = ? , user_id = ? WHERE id = ?",
        (updated_task.title, updated_task.completed, updated_task.user_id, task_id) 
    )

    if not cursor.rowcount:
        conn.close()    
        raise HTTPException(status_code=404, detail="Task doesn't exist")
    
    conn.commit()
    conn.close()

    return {"message": "Task updated successfully"}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Task doesn't exist")
    
    conn.commit()
    conn.close()

    return {"message": "Task deleted successfully"}
    