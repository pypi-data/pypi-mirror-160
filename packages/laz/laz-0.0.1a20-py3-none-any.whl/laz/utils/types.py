# std
from typing import Dict, List, Union

# external
from prodict import Prodict

# type definitions
AtomicData = Union[type(None), bool, int, str]
ListData = List[Union[AtomicData, 'ListData', 'DictData']]
_DictData = Dict[str, Union[AtomicData, ListData, 'DictData']]
_ProdictData = Prodict[str, Union[AtomicData, ListData, 'DictData']]
DictData = Union[_DictData, _ProdictData]
Data = Union[AtomicData, ListData, DictData]
