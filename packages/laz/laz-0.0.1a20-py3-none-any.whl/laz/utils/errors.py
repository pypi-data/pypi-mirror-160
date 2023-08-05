# external
from botocore.exceptions import ClientError


class LazError(Exception):
    pass


class LazValueError(LazError, ValueError):
    pass


class LazTypeError(LazError, TypeError):
    pass


class LazBoto3ClientError(LazError, ClientError):

    @classmethod
    def raise_if_bad_status(cls, response: dict):
        response_metadata = response['ResponseMetadata']
        if response_metadata['HTTPStatusCode'] >= 300:
            error_response = {
                'Code': response_metadata['HTTPStatusCode'],
            }
            operation_name = '???'
            raise LazBoto3ClientError(error_response, operation_name)


class LazRuntimeError(LazError, RuntimeError):
    pass


class LazActionError(LazRuntimeError):
    pass
