import uvicorn
from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException

from api.database import get_db_session
from api.task import Task
from api.task_repository import TaskRepository
from api.task_repository_interface import TaskRepositoryInterface


def create_app() -> FastAPI:
    return FastAPI()


app = create_app()


def get_task_repository(db=Depends(get_db_session)) -> TaskRepositoryInterface:
    return TaskRepository(db=db)


@app.post("/tasks/", response_model=Task)
def create_task(
    task: Task, task_repository: TaskRepositoryInterface = Depends(get_task_repository)
) -> Task:
    existing_task = task_repository.get_task_by_title(title=task.title)
    if existing_task:
        raise HTTPException(status_code=400, detail=f"task : {task.title} already exists.")
    return task_repository.create_task(task=task)


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(
    task_id: int, task_repository: TaskRepositoryInterface = Depends(get_task_repository)
) -> Task:
    task = task_repository.get_task_by_id(task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"task with id {task_id} not found.")
    return task


@app.get("/tasks/", response_model=list[Task])
def get_tasks(
    skip: int = 0,
    limit: int = 100,
    task_repository: TaskRepositoryInterface = Depends(get_task_repository),
) -> list[Task]:
    return task_repository.get_tasks(skip=skip, limit=limit)


@app.post("/tasks/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    task: Task,
    task_repository: TaskRepositoryInterface = Depends(get_task_repository),
) -> Task:
    existing_task = task_repository.get_task_by_id(task_id=task_id)
    if not existing_task:
        raise HTTPException(status_code=404, detail=f"task with id {task_id} not found.")
    return task_repository.update_task(task=task, task_id=task_id)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=1111)
