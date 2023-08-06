from dataclasses import dataclass

from lambler.resource.role import Role


@dataclass
class LambdaFunctionMetadata:
    name: str
    function_url: str
    role: Role
