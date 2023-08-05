# std
from typing import Callable, Dict, List, Optional as Opt

# internal
from laz.utils.errors import LazTypeError
from laz.utils.types import Data, AtomicData, DictData, ListData


class Walk:

    def __init__(
            self,
            data: Data,
            context: Opt[DictData] = None,
            atomic_handler: Opt[Callable[[AtomicData, Opt[DictData]], Data]] = None,
            dict_handler: Opt[Callable[[Dict, Opt[DictData]], Data]] = None,
            list_handler: Opt[Callable[[List, Opt[DictData]], Data]] = None,
    ):
        self.data = data
        self.context = context
        self.atomic_handler = atomic_handler
        self.dict_handler = dict_handler
        self.list_handler = list_handler

    def walk(self):
        return self._walk(self.data)

    def _walk(self, data: Data):
        if isinstance(data, dict):
            return self._walk_dict(data)
        elif isinstance(data, list):
            return self._walk_list(data)
        elif isinstance(data, (type(None), bool, int, str)):
            return self._walk_atomic(data)
        else:
            raise LazTypeError(f'Cannot walk input of type {type(data)}')

    def _walk_dict(self, data: DictData):
        for key in data.keys():
            data[key] = self._walk(data[key])
        if self.dict_handler is not None:
            return self.dict_handler(data, self.context)
        return data

    def _walk_list(self, data: ListData):
        for i in range(len(data)):
            data[i] = self._walk(data[i])
        if self.list_handler is not None:
            return self.list_handler(data, self.context)
        return data

    def _walk_atomic(self, data: AtomicData):
        if self.atomic_handler is not None:
            return self.atomic_handler(data, self.context)
        return data
