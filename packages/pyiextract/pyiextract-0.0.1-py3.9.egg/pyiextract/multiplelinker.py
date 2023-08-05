import typing

from .linker import Linker
from .entity import Entity


class MultipleLinker(Linker):
    def __init__(self, linkers: typing.List[Linker]) -> None:
        super().__init__("multiple")
        self._linkers = linkers

    def link(self, entity: typing.Any, sentence: typing.Any) -> Entity:
        last_linked_entity = None
        for linker in self._linkers:
            last_linked_entity = linker.link(entity, sentence)
            if last_linked_entity.identifier() == last_linked_entity.name():
                continue
            return last_linked_entity
        return last_linked_entity
