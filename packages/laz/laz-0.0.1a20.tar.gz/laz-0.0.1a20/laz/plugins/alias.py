# std
from copy import deepcopy

# internal
from laz.utils.types import AtomicData, Data, DictData
from laz.plugins.plugin import Plugin
from laz.utils.walk import Walk


class AliasPlugin(Plugin):

    def before_target(self):
        aliased = alias(self.context.data)
        self.context.replace(aliased)


def alias(data: DictData) -> Data:
    data = deepcopy(data)
    return _alias(data, data)


def _alias(data: DictData, context: DictData) -> Data:
    walk = Walk(data, context, atomic_handler=_handle_atomic)
    return walk.walk()


def _handle_atomic(data: AtomicData, context: DictData) -> Data:
    if isinstance(data, str):
        if data.startswith('='):
            for key, val in context.items():
                locals()[key] = val
            result = _alias(eval(data[1:]), context)
            return result
    return data
