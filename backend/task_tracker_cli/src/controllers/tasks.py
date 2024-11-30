from typing import List, Optional

from ..models import Task, TaskStatus, TaskStorage


class TaskCRUD:
    store: TaskStorage

    def __init__(self, store: TaskStorage):
        self.store = store

    def add(self, desc: str, status: Optional[TaskStatus] = None) -> Task:
        self.store.index += 1
        new_task = Task(
            id=self.store.index, description=desc, status=status or TaskStatus.PENDING
        )
        self.store.items[new_task.id] = new_task

        return new_task

    def update(
        self,
        task_id: int,
        *,
        desc: Optional[str] = None,
        status: Optional[TaskStatus] = None,
    ) -> Task:
        attrs = (("description", desc), ("status", status))
        task = self.store.items[task_id]

        for key, value in attrs:
            if value is None:
                continue

            setattr(task, key, value)

        return task

    def delete(self, task_id: int) -> Task:
        return self.store.items.pop(task_id)

    def get_list(self, statuses: Optional[List[TaskStatus]] = None) -> List[Task]:
        if statuses is None:
            return list(self.store.items.values())

        tasks = [task for task in self.store.items.values() if task.status in statuses]

        return tasks
