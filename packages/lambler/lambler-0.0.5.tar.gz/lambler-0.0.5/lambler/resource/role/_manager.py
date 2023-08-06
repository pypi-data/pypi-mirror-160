import json
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class RoleMetadata:
    name: str
    arn: str


class RoleManager:
    def __init__(self, client):
        self._client = client

    def create(self, name: str, policy: Dict[str, Any]) -> RoleMetadata:
        response = self._client.create_role(
            RoleName=name,
            AssumeRolePolicyDocument=json.dumps(policy),
        )
        return RoleMetadata(name, response["Role"]["Arn"])

    def attach_policy(self, name: str, policy_arn: str):
        self._client.attach_role_policy(
            PolicyArn=policy_arn,
            RoleName=name,
        )

    def delete_cascade(self, name: str):
        response = self._client.list_attached_role_policies(
            RoleName=name,
        )
        arn_list = [policy["PolicyArn"] for policy in response["AttachedPolicies"]]

        for arn in arn_list:
            self._client.detach_role_policy(RoleName=name, PolicyArn=arn)

        self._client.delete_role(RoleName=name)

    @staticmethod
    def from_arn(arn: str) -> RoleMetadata:
        name = arn.split("/")[-1]
        return RoleMetadata(name, arn)

    def get_role(self, name: str) -> RoleMetadata:
        response = self._client.get_role(RoleName=name)
        return RoleMetadata(name, response["Role"]["Arn"])
