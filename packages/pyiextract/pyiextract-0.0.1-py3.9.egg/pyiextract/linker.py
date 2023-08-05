import typing

from .node import Node
from .entity import Entity


class Linker(Node):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def link(self, entity: typing.Any, sentence: typing.Any) -> Entity:
        entity_name = str(entity)
        return Entity(entity_name, entity_name)

    def name(self) -> str:
        return super().name() + "-linker"
