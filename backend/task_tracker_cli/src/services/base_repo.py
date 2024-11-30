import json
import os
from functools import update_wrapper

from typing import TextIO, Optional, TypeVar, Generic, Type

from pydantic import BaseModel


TStorage = TypeVar("TStorage")


def with_open_db(func):
    def wrapper(cls: "BaseJsonRepo", *args, **kwargs):
        if not cls.is_open:
            raise Exception("Can't get access to closed database")

        return func(cls, *args, **kwargs)

    return update_wrapper(wrapper, func)


class BaseJsonRepo(Generic[TStorage]):
    __filepath: str
    __fp: Optional[TextIO] = None
    _db: Optional[BaseModel] = None
    _model: Type[TStorage]

    def __init__(self, filepath: str):
        if not filepath:
            raise ValueError("Filepath cannot be empty")

        self.__filepath = filepath

    def init_db(self, data):
        return self._model.model_validate(data)

    @property
    def is_open(self) -> bool:
        return self.__fp is not None and not self.__fp.closed

    @property
    def db(self):
        return self._db

    @with_open_db
    def commit(self):
        self.__fp.seek(0)
        self.__fp.truncate()
        json.dump(
            self.db.model_dump(mode="json"),
            self.__fp,  # noqa
            indent=4,
        )

    def open(self):
        self.__fp = open(self.__filepath, "a+")
        self.__fp.seek(0)
        data = json.load(self.__fp) if os.stat(self.__filepath).st_size else {}
        self._db = self.init_db(data)

    def close(self):
        self.commit()

        self.__fp.close()
        self.__fp = None
        self._db = None

    def __enter__(self) -> None:
        self.open()

    def __exit__(self, *_) -> None:
        self.close()

    def __del__(self) -> None:
        if self.is_open:
            self.__fp.close()
