from typing import Optional

from lambler.resource.function._metadata import LambdaFunctionMetadata
from lambler.resource.role import Role, get_role_from_arn


class LambdaManager:
    def __init__(self, client):
        self._client = client

    def is_lambda_function_exists(self, name: str) -> bool:
        try:
            self.get_lambda_function(name)
        except self._client.exceptions.ResourceNotFoundException:
            return False
        return True

    def create(self, name: str, zip_file_path: str, handler_name: str,
               role: Role) -> LambdaFunctionMetadata:
        zip_file = _read_zip_file_content(zip_file_path)

        self._create_lambda_function(name, role, handler_name, zip_file)
        function_url = self._create_lambda_function_public_url(name)

        return LambdaFunctionMetadata(name, function_url, role)

    def delete(self, name: str):
        self._client.delete_function_url_config(
            FunctionName=name,
        )
        self._client.delete_function(
            FunctionName=name,
        )

    def get_lambda_function(self, name: str) -> Optional[LambdaFunctionMetadata]:
        try:
            response = self._client.get_function(
                FunctionName=name,
            )
        except self._client.exceptions.ResourceNotFoundException:
            return None

        role = get_role_from_arn(arn=response["Configuration"]["Role"])

        response = self._client.get_function_url_config(FunctionName=name)
        url = response["FunctionUrl"]

        return LambdaFunctionMetadata(name, url, role)

    def _create_lambda_function_public_url(self, name):
        response = self._client.create_function_url_config(
            FunctionName=name,
            AuthType="NONE",
        )
        function_url = response['FunctionUrl']

        self._client.add_permission(
            Action="lambda:InvokeFunctionUrl",
            FunctionName=name,
            Principal="*",
            StatementId="FunctionURLAllowPublicAccess",
            FunctionUrlAuthType="NONE",
        )

        return function_url

    def _create_lambda_function(self, name, role, handler_name, zip_file):
        self._client.create_function(
            FunctionName=name,
            Runtime='python3.9',
            Role=role.arn,
            Handler=handler_name,
            Code=dict(ZipFile=zip_file),
        )


def _read_zip_file_content(zip_file_path: str):
    with open(zip_file_path, 'rb') as file:
        zip_file = file.read()
    return zip_file
