from pydantic import BaseModel, Field

from .base_repo import BaseJsonRepo
from ..models.task import TaskStorage


class GlobalJsonStorage(BaseModel):
    TASKS: TaskStorage = Field(default_factory=lambda: TaskStorage())


class AppJsonRepo(BaseJsonRepo[GlobalJsonStorage]):
    _model = GlobalJsonStorage
