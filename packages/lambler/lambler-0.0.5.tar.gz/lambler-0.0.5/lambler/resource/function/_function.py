from lambler.resource.function._manager import LambdaManager
from ..role import Role


class LambdaFunction:
    def __init__(self, manager: LambdaManager, name: str, url: str, role: Role):
        self._manager = manager
        self._name = name
        self._url = url
        self._role = role

    @property
    def url(self) -> str:
        return self._url

    def delete_cascade(self):
        self._manager.delete(self._name)
        self._role.delete()
