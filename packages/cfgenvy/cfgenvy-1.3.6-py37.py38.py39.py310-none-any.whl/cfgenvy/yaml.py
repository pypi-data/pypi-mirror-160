# -*- coding: utf-8 -*-
"""Yaml."""

from __future__ import annotations

from logging import getLogger
from typing import Any, Dict, Callable, Optional, Pattern, Type

from yaml import dump as _yaml_dumps
from yaml import load as _yaml_loads

try:
    from yaml import CSafeDumper as MyDumper  # type: ignore[misc]
    from yaml import CSafeLoader as MyLoader  # type: ignore[misc]
except ImportError:
    from yaml import SafeDumper as MyDumper  # type: ignore[misc]
    from yaml import SafeLoader as MyLoader  # type: ignore[misc]

logger = getLogger(__name__)


def yaml_dump(data: Any, path: str, **kwargs) -> None:
    """Dump yaml file."""
    with open(path, "w", encoding="utf-8") as fout:
        yaml_dumps(data=data, stream=fout, **kwargs)


def yaml_load(path: str):
    """Load yaml file."""
    with open(path, encoding="utf-8") as fin:
        return yaml_loads(fin)


def yaml_dumps(
    data,
    *,
    Dumper: Optional[Type[MyDumper]] = None,  # noqa: N803
    **kwargs,
):
    """Yaml dumps.

    Include our Dumper. Clients do not have to repeat the try...except
        import for CSafeDumper above.
    """
    return _yaml_dumps(data=data, Dumper=Dumper or MyDumper, **kwargs)


def yaml_loads(
    stream,
    *,
    Loader: Optional[Type[MyLoader]] = None,  # noqa: N803
):
    """Yaml loads.

    Include our Loader. Clients do not have to repeat the try...except
        import for CSafeLoader above.
    """
    return _yaml_loads(stream=stream, Loader=Loader or MyLoader)


def yaml_type(
    cls: type,
    tag: str,
    *,
    init: Optional[Callable] = None,
    repr: Optional[Callable] = None,  # pylint: disable=redefined-builtin
    loader: Optional[Type[MyLoader]] = None,
    dumper: Optional[Type[MyDumper]] = None,
    **kwargs,
):
    """Yaml type."""
    _loader = loader or MyLoader
    _dumper = dumper or MyDumper
    if init is not None:

        def _init_closure(loader, node):
            return init(loader, node, **kwargs)

        _loader.add_constructor(tag, _init_closure)

    if repr is not None:

        def _repr_closure(dumper, self):
            return repr(dumper, self, tag=tag, **kwargs)

        _dumper.add_representer(cls, _repr_closure)


def yaml_implicit_type(
    cls: type,
    tag: str,
    *,
    init: Callable,
    pattern: Pattern,
    repr: Optional[Callable] = None,  # pylint: disable=redefined-builtin
    loader: Optional[Type[MyLoader]] = None,
    dumper: Optional[Type[MyDumper]] = None,
    **kwargs,
):
    """Yaml implicit type."""
    _loader = loader or MyLoader
    _dumper = dumper or MyDumper

    def _init_closure(loader, node):
        return init(loader, node, pattern=pattern, **kwargs)

    _loader.add_constructor(tag, _init_closure)
    _loader.add_implicit_resolver(tag, pattern, None)

    if repr is not None:

        def _repr_closure(dumper, self):
            return repr(dumper, self, tag=tag, pattern=pattern, **kwargs)

        _dumper.add_representer(cls, _repr_closure)


class Mapping:
    """Mapping."""

    YAML = "!mapping"

    @classmethod
    def as_yaml_type(cls, tag: Optional[str] = None) -> None:
        """As yaml type."""
        yaml_type(
            cls,
            tag or cls.YAML,
            init=cls._yaml_init,
            repr=cls._yaml_repr,
        )

    @classmethod
    def _yaml_init(cls, loader, node) -> Any:
        """Yaml init."""
        return cls(**loader.construct_mapping(node, deep=True))

    @classmethod
    def _yaml_repr(cls, dumper, self, *, tag: str) -> str:
        """Yaml repr."""
        return dumper.represent_mapping(tag, self.as_yaml())

    def as_yaml(self) -> Dict[str, Any]:
        """As yaml."""
        raise NotImplementedError()
