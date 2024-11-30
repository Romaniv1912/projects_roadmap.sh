from datetime import datetime
from enum import Enum, unique

from pydantic import ConfigDict, BaseModel, Field, model_validator


NOW_FACTORY = datetime.now
TASK_ITEMS_STORAGE = dict[int, "Task"]


class TaskStorage(BaseModel):
    index: int = Field(default=0)
    items: TASK_ITEMS_STORAGE = Field(default_factory=TASK_ITEMS_STORAGE)  # noqa # TODO: fix factory bug


@unique
class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"


class Task(BaseModel):
    id: int
    description: str
    status: TaskStatus
    created_at: datetime = Field(default_factory=NOW_FACTORY)
    updated_at: datetime = Field(default_factory=NOW_FACTORY)

    model_config = ConfigDict(validate_assignment=True)

    @model_validator(mode="after")
    def number_validator(self) -> "Task":
        self.model_config["validate_assignment"] = False

        self.updated_at = NOW_FACTORY()

        self.model_config["validate_assignment"] = True

        return self
