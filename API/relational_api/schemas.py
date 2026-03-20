from pydantic import BaseModel

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