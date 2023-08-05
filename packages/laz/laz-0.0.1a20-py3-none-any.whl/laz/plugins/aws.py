# std
from copy import deepcopy
import json
import os
from typing import Dict, Union

# external
import boto3

# internal
from laz.utils.errors import LazValueError, LazError, LazBoto3ClientError
from laz.utils import log
from laz.utils.types import Data
from laz.utils.contexts import with_environ
from laz.utils.funcs import compact_dict
from laz.model.action import Action
from laz.model.configuration import Configuration
from laz.model.target import Target
from laz.plugins.plugin import Plugin


class AwsPlugin(Plugin):
    _secret_string_cache: Dict[str, str] = {}

    @property
    def config(self):
        return self.context.data.get('aws') or {}

    def before_all(self):
        env = {}
        aws_profile = self.config.get('profile')
        if aws_profile is not None:
            env['AWS_PROFILE'] = aws_profile
        aws_region = self.config.get('region')
        if aws_region is not None:
            env['AWS_DEFAULT_REGION'] = aws_region
        if env:
            self.push_env(**env)

    def before_target(self):
        self._handle_secrets()

    def _handle_secrets(self):
        env = {}
        for key, val in self.env.items():
            if isinstance(val, dict) and len(val.keys()) == 1 and 'aws' in val and isinstance(val['aws'], dict):
                secret_config = val['aws']
                env[key] = self._get_secret_value(secret_config)
        if env:
            data = deepcopy(self.context.data)
            for key, val in env.items():
                data['env'][key] = val
            self.context.replace(data)

    def _get_secret_value(self, secret_config: dict) -> str:
        profile_name = secret_config.get('profile_name') or self.env.get('AWS_PROFILE')
        region_name = secret_config.get('region_name') or self.env.get('AWS_DEFAULT_REGION')
        secret_id = secret_config.get('secret_id')
        version_id = secret_config.get('version_id')
        version_stage = secret_config.get('version_stage')
        json_key = secret_config.get('json_key')
        cache_id = '|'.join(map(str, (profile_name, region_name, secret_id, version_id, version_stage)))
        if cache_id in self._secret_string_cache:
            log.debug(f'Getting cached AWS secret: {cache_id}')
            secret_string = self._secret_string_cache[cache_id]
        else:
            log.debug(f'Getting AWS secret: {secret_config}')
            session = boto3.Session(profile_name=profile_name, region_name=region_name)
            client = session.client('secretsmanager')
            response = client.get_secret_value(**compact_dict(dict(
                SecretId=secret_id,
                VersionId=version_id,
                VersionStage=version_stage,
            )))
            LazBoto3ClientError.raise_if_bad_status(response)
            secret_string = response['SecretString']
            self._secret_string_cache[cache_id] = secret_string
        if json_key:
            return json.loads(secret_string)[json_key]
        else:
            return secret_string


class AwsAction(Action):

    def run(self):
        if isinstance(self.run_data['aws'], dict) and 'assume_role' in self.run_data['aws']:
            return self._assume_role()
        elif isinstance(self.run_data['aws'], dict):
            return self._arbitrary_aws_action()
        else:
            raise LazValueError(f'Invalid aws plugin action')

    def _assume_role(self):
        import boto3
        aws: dict = self.run_data['aws']
        kwargs: Dict[str, str] = aws['assume_role']
        if 'RoleSessionName' not in kwargs:
            kwargs['RoleSessionName'] = os.environ['USER']
        with with_environ(self.context.data.get('env', {})):
            sts = boto3.client('sts')
            response = sts.assume_role(**kwargs)
        status_code = response['ResponseMetadata']['HTTPStatusCode']
        if status_code >= 300:
            raise LazError(f'Assume Role Error: HTTPStatusCode {status_code}')
        credentials = response['Credentials']
        self.env(
            AWS_ACCESS_KEY_ID=credentials['AccessKeyId'],
            AWS_SECRET_ACCESS_KEY=credentials['SecretAccessKey'],
            AWS_SESSION_TOKEN=credentials['SessionToken'],
        )

    def _arbitrary_aws_action(self):
        import boto3
        with with_environ(self.context.data.get('env') or {}):
            aws: Dict[str, Dict[str, Dict[str, str]]] = self.run_data['aws']
            service: str = list(aws.keys())[0]
            subcommand: str = list(aws[service].keys())[0]
            kwargs: Dict[str, str] = aws[service][subcommand] or {}
            client = boto3.client(service)
            method = getattr(client, subcommand)
            response = method(**kwargs)
        response_metadata = response.pop('ResponseMetadata')
        status_code = response_metadata['HTTPStatusCode']
        if status_code >= 300:
            log.error(str(aws))
            log.error(str(response))
            raise LazError(f'AWS action failed')
        print(json.dumps(response, indent=2))
        return response

    @classmethod
    def is_handler(cls, context: Union[Configuration, Target], run_data: Data) -> bool:
        return isinstance(run_data, dict) and 'aws' in run_data
