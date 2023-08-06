import inspect
from abc import abstractmethod, ABC
from typing import Dict, TypeVar, Type

from lambler import content
from lambler.content import ContentProviderSpace, Content
from ._template import Template

T = TypeVar("T", bound="TemplateBase")


def build_marked_params(content_providers: ContentProviderSpace, type_: Type):
    assert issubclass(type_, TemplateBase)
    return type_.do_load(content_providers)


class TemplateBase(ABC):

    @classmethod
    @abstractmethod
    def load(cls: Type[T], *args, **kwargs) -> T:
        pass

    @classmethod
    def do_load(cls: Type[T], content_providers: ContentProviderSpace) -> T:
        return cls.load(**_extract_template_params(inspect.signature(cls.load), content_providers))


def _extract_template_params(signature: inspect.Signature, content_providers: ContentProviderSpace) -> Dict:
    params = {}
    for name, param in signature.parameters.items():
        type_ = param.annotation
        marker = param.default
        if isinstance(marker, Content):
            value = content.build_marked_params(content_providers, marker)
        elif isinstance(marker, Template):
            value = build_marked_params(content_providers, type_)
        else:
            raise NotImplementedError()
        params[name] = value
    return params
