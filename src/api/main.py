from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

app = FastAPI(title="Task Manager API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Priority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    URGENT = "Urgent"

class TaskBase(BaseModel):
    title: str
    description: str
    category: str = "General"
    priority: Priority = Priority.MEDIUM
    due_date: Optional[datetime] = None
    dependencies: List[int] = []

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    completed: bool = False

    class Config:
        from_attributes = True

# In-memory storage (will be replaced with database)
tasks = []
next_id = 1

@app.get("/tasks/", response_model=List[Task])
async def get_tasks(category: Optional[str] = None, priority: Optional[Priority] = None):
    filtered_tasks = tasks
    if category:
        filtered_tasks = [t for t in filtered_tasks if t.category == category]
    if priority:
        filtered_tasks = [t for t in filtered_tasks if t.priority == priority]
    return filtered_tasks

@app.post("/tasks/", response_model=Task)
async def create_task(task: TaskCreate):
    global next_id
    new_task = Task(
        id=next_id,
        **task.model_dump()
    )
    tasks.append(new_task)
    next_id += 1
    return new_task

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    task = next((t for t in tasks if t.id == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}/complete")
async def complete_task(task_id: int):
    task = next((t for t in tasks if t.id == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Check dependencies
    for dep_id in task.dependencies:
        dep_task = next((t for t in tasks if t.id == dep_id), None)
        if dep_task and not dep_task.completed:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot complete task: dependency {dep_id} is not completed"
            )
    
    task.completed = True
    return {"message": "Task completed successfully"}

@app.get("/categories/")
async def get_categories():
    return list(set(task.category for task in tasks))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 