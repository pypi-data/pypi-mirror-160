# std
from copy import deepcopy
import json
from typing import Optional as Opt

# external
from jinja2 import Environment

# internal
from laz.utils.errors import LazTypeError
from laz.utils.types import AtomicData, Data, DictData, ListData
from laz.plugins.plugin import Plugin

# custom jinja filters
def jsonify2(x):
    return json.dumps(json.dumps(x))

# jinja environment
env = Environment()
env.filters['jsonify'] = json.dumps
env.filters['jsonify2'] = jsonify2


class JinjaPlugin(Plugin):

    def before_target(self):
        evaluated = _evaluate(self.context.data)
        self.context.replace(evaluated)


def _evaluate(data: Data, variables: Opt[DictData] = None) -> Data:
    if variables is None and isinstance(data, dict):
        variables = data
    data = deepcopy(data)
    return _expand(data, variables)


def _expand(data: Data, variables: DictData) -> Data:
    if isinstance(data, dict):
        return _expand_dict(data, variables)
    elif isinstance(data, list):
        return _expand_list(data, variables)
    elif isinstance(data, (type(None), bool, int, str)):
        return _expand_atomics(data, variables)
    else:
        raise LazTypeError(f'Cannot expand input of type {type(data)}')


def _expand_dict(data: DictData, variables: DictData) -> DictData:
    for key in data.keys():
        data[key] = _expand(data[key], variables)
    return data


def _expand_list(data: ListData, variables: DictData) -> ListData:
    for i in range(len(data)):
        data[i] = _expand(data[i], variables)
    return data


def _expand_atomics(data: AtomicData, variables: DictData) -> AtomicData:
    if isinstance(data, str):
        previous = data
        while True:
            template = env.from_string(previous)
            rendered = template.render(**variables)
            if rendered == previous:
                break
            else:
                previous = rendered
        return rendered
    else:
        return data
