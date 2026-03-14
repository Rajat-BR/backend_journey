# Task CRUD API

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Task(BaseModel):
    title: str
    completed: bool = False

tasks = []

@app.get("/")
def home():
    return {"message": "Welcome to the CRUD API"}


@app.post("/tasks")
def create_task(new_task: Task):

    new_task = {
        "id": len(tasks)+1,
        "title": new_task.title,
        "completed": new_task.completed
    }

    tasks.append(new_task)
    return {"message": "Task added successfully"}


@app.get("/tasks")
def fetch_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def fetch_tasks_by_id(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    
    raise HTTPException(status_code=404, detail="Task not Found")


@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = updated_task.title
            task["completed"] = updated_task.completed
            return {"message": f"Task {id} updated successfully"}
    
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message": f"Task {task_id} deleted successfully"}
    
    raise HTTPException(status_code=404, detail="Task not found")