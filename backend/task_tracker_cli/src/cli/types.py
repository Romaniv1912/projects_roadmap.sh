from typing import Optional, TypeVar, Generic, List

from ..models import Task

TVal = TypeVar("TVal")


class Result(Generic[TVal]):
    def __init__(
        self,
        *,
        msg: Optional[str] = None,
        value: Optional[TVal] = None,
        priority: int = 0,
    ):
        self.msg = msg
        self.value = value
        self.priority = priority


class TaskResult(Result[List[Task] | Task]):
    pass
