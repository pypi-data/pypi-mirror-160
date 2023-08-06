import time

# noinspection PyPackageRequirements
import boto3

from lambler.resource.function._manager import LambdaManager
from lambler.resource.role import get_or_create_lambda_function_role
from ._function import LambdaFunction


def get_or_create_lambda_function(name: str, zip_file: str, handler_name: str) -> LambdaFunction:
    manager = LambdaManager(boto3.client("lambda"))
    fn = manager.get_lambda_function(name)
    if fn is None:
        role = get_or_create_lambda_function_role("LamblerBasicExecution")
        time.sleep(20)  # TODO: use wait-for or retry loop
        fn = manager.create(name, zip_file, handler_name, role)

    return LambdaFunction(manager, name, fn.function_url, fn.role)
