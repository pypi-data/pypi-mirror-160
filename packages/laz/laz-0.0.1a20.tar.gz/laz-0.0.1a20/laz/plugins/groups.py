# std
from typing import Dict, List

# internal
from laz.utils.types import AtomicData, Data, DictData
from laz.model.path import Path
from laz.plugins.plugin import Plugin


class GroupsPlugin(Plugin):

    @property
    def groups(self) -> Dict[str, List[str]]:
        return self.context.data.get('groups') or {}

    @property
    def path(self) -> Path:
        return Path(
            self.context.data['path'],
            **self.context.data['laz'],
        )

    def before_all(self):
        path = self.path
        base = path.base
        groups = self.groups
        if base in groups:
            new_base = '{' + ','.join(self.groups[base]) + '}'
            path.base = new_base
            self.context.push({'path': path.value})
