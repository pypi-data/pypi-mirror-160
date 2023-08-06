from lambler.resource.role._manager import RoleManager


class Role:
    def __init__(self, manager: RoleManager, name: str, arn: str):
        self._manager = manager
        self._name = name
        self._arn = arn

    @property
    def arn(self) -> str:
        return self._arn

    def delete(self):
        self._manager.delete_cascade(self._name)

    def attach_policy(self, policy_arn: str):
        self._manager.attach_policy(self._name, policy_arn)
