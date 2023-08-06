# noinspection PyPackageRequirements
import boto3

from ._manager import RoleManager
from ._role import Role


def get_or_create_lambda_function_role(name: str) -> Role:
    client = boto3.client('iam')
    manager = RoleManager(client)
    try:
        metadata = manager.get_role(name)
        role = Role(manager, metadata.name, metadata.arn)
    except client.exceptions.NoSuchEntityException:
        role = create_lambda_function_role(name)

    return role


def create_lambda_function_role(name: str) -> Role:
    manager = RoleManager(boto3.client('iam'))

    role_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "",
                "Effect": "Allow",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }

    metadata = manager.create(name, role_policy)

    role = Role(manager, metadata.name, metadata.arn)
    role.attach_policy("arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole")

    return role


def get_role_from_arn(arn: str) -> Role:
    manager = RoleManager(boto3.client('iam'))
    metadata = manager.from_arn(arn)
    return Role(manager, metadata.name, metadata.arn)
