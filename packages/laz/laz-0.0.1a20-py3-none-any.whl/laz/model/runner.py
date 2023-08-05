# std
import argparse
from typing import List

# internal
from laz.utils import log
from laz.utils.contexts import in_dir
from laz.model.tree import Node
from laz.model.path import Path
from laz.model.resolver import Resolver
from laz.model.configuration import Configuration
from laz.model.target import Target
from laz.model.act import Act
from laz.model.action import Action
from laz.plugins.plugin import PLUGINS


class Runner:

    def __init__(self, root_node: Node, cli_args: argparse.Namespace, args: List[str]):
        self.root_node = root_node
        config = self.root_node.configuration.data.get('laz') or {}
        self.error_on_no_targets = config['error_on_no_targets']
        self.cli_args = cli_args
        self.root_node.configuration.push({
            'path': args[0],
            'args': args[1:],
        })

    def resolve(self) -> List[Target]:
        path = Path(
            self.root_node.configuration.data['path'],
            **self.root_node.configuration.data['laz'],
        )
        resolver = Resolver(self.root_node, path)
        targets = resolver.resolve()
        if self.cli_args.reverse:
            targets.reverse()
        return targets

    def run(self):
        self.load_plugins(self.root_node.configuration)
        self.before_all(self.root_node.configuration)
        targets = self.resolve()
        if len(targets) == 0:
            msg = 'Given path resolved to zero targets'
            if self.error_on_no_targets:
                log.error(msg)
                exit(1)
            else:
                log.warning(msg)
        for target in targets:
            self._run_target(target)
        self.after_all(self.root_node.configuration)

    def _run_target(self, target: Target):
        log.debug(f'Running target {target.id}')
        with in_dir(target.data['config']['dirpath']):
            args = target.data['args']
            if len(args) == 0:
                default_action = target.data['laz']['default_action']
                log.debug(f'Running default action: {default_action}')
                args += [default_action]
                target.data['args'] = args
            self.before_target(target)
            act = Act.new(target, args=' '.join(target.data['args']))
            act.act()
            self.after_target(target)

    @staticmethod
    def load_plugins(configuration: Configuration):
        from importlib import import_module
        plugins = configuration.data.get('plugins', [])
        for import_path in plugins:
            import_module(import_path)

    @staticmethod
    def before_all(configuration: Configuration):
        log.debug(f'Running before_all hooks')
        for Plugin in PLUGINS:
            try:
                plugin = Plugin(configuration)
                plugin.before_all()
            except NotImplementedError:
                pass
        hook = configuration.data.get('hooks', {}).get('before_all')
        if hook is not None:
            action = Action.new(configuration, hook)
            act = Act(configuration, action=action)
            act.act()

    @staticmethod
    def before_target(target: Target):
        log.debug(f'Running before_target hooks')
        for Plugin in PLUGINS:
            try:
                plugin = Plugin(target)
                plugin.before_target()
            except NotImplementedError:
                pass
        hook = target.data.get('hooks', {}).get('before_target')
        if hook is not None:
            action = Action.new(target, hook)
            act = Act(target, action=action)
            act.act()

    @staticmethod
    def after_target(target: Target):
        log.debug(f'Running after_target hooks')
        for Plugin in PLUGINS:
            try:
                plugin = Plugin(target)
                plugin.after_target()
            except NotImplementedError:
                pass
        hook = target.data.get('hooks', {}).get('after_target')
        if hook is not None:
            action = Action.new(target, hook)
            act = Act(target, action=action)
            act.act()

    @staticmethod
    def after_all(configuration: Configuration):
        log.debug(f'Running after_all hooks')
        for Plugin in PLUGINS:
            try:
                plugin = Plugin(configuration)
                plugin.after_all()
            except NotImplementedError:
                pass
        hook = configuration.data.get('hooks', {}).get('after_all')
        if hook is not None:
            action = Action.new(configuration, hook)
            act = Act(configuration, action=action)
            act.act()
