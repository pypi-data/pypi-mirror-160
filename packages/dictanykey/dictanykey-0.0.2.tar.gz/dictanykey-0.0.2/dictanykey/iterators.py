from typing import Any, Iterator, Protocol


class AnyKeyMapping(Protocol):
    def __len__(self) -> int:
        ...

    def _get_keys_list(self) -> list:
        ...

    def _get_values_list(self) -> list:
        ...

    def _get_items_list(self) -> list[tuple]:
        ...


class ViewIterator:
    def __init__(self, parent: AnyKeyMapping) -> None:
        self.parent: AnyKeyMapping = parent
        self.len: int = len(parent)

    def __next__(self) -> Any:
        if len(self.parent) != self.len:
            raise RuntimeError('dictionary changed size during iteration')
        return next(self.iterator)


class DictKeyIterator(ViewIterator):
    def __init__(self, parent: AnyKeyMapping) -> None:
        super().__init__(parent)
        self.iterator: Iterator = iter(parent._get_keys_list())
    
    
class DictValueIterator(ViewIterator):
    def __init__(self, parent: AnyKeyMapping) -> None:
        super().__init__(parent)
        self.iterator: Iterator = iter(parent._get_values_list())
    
    
class DictItemIterator(ViewIterator):
    def __init__(self, parent: AnyKeyMapping):
        super().__init__(parent)
        self.iterator: Iterator = iter(parent._get_items_list())