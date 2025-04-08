from abc import ABC, abstractmethod

from api.models import Task as TaskModel
from api.task import Task


class TaskRepositoryInterface(ABC):
    @abstractmethod
    def get_task_by_id(self, user_id: int) -> Task | None:
        pass

    @abstractmethod
    def get_tasks(self, skip: int = 0, limit: int = 100) -> list[Task]:
        pass

    @abstractmethod
    def create_task(self, task: TaskModel) -> Task:
        pass

    @abstractmethod
    def update_task(self, task: TaskModel) -> Task:
        pass
