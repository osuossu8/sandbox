from sqlalchemy.orm import Session

from api.models import Task as TaskModel
from api.task import Task
from api.task_repository_interface import TaskRepositoryInterface


class TaskRepository(TaskRepositoryInterface):
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_task_by_id(self, task_id: int) -> Task | None:
        return self.db.query(TaskModel).filter(TaskModel.id == task_id).first()

    def get_task_by_title(self, title: str) -> Task | None:
        return self.db.query(TaskModel).filter(TaskModel.title == title).first()

    def get_tasks(self, skip: int = 0, limit: int = 100) -> list[Task]:
        return self.db.query(TaskModel).offset(skip).limit(limit).all()

    def create_task(self, task: Task) -> Task:
        new_task = TaskModel(**task.model_dump())
        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)
        return Task.model_validate(new_task)

    def update_task(self, task: Task, task_id: int) -> Task:
        existing_task = self.db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if existing_task:
            for key, value in task.model_dump().items():
                setattr(existing_task, key, value)
            self.db.commit()
            self.db.refresh(existing_task)
            return Task.model_validate(existing_task)
        return None
