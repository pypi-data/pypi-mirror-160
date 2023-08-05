# std
from copy import deepcopy
from typing import Union

# external
from prodict import Prodict

# internal
from laz.utils.types import Data, DictData
from laz.utils.walk import Walk


def prodictify(data: Data) -> Union[Data, Prodict]:
    data = deepcopy(data)
    walk = Walk(data, data, dict_handler=_handle_dict)
    return walk.walk()


def _handle_dict(data: DictData, _) -> Prodict:
    return Prodict.from_dict(data)
