from typing import Any, Iterable, Iterator, Mapping, Optional
from dictanykey.utils import quote_string


class MappingMixin:
    def __getitem__(self, key: Any) -> Any:
        if key in self._get_keys_list():
            return self.get(key)
        else:
            raise KeyError(key)

    def __str__(self) -> str:
        d = ', '.join(f'{quote_string(key)}: {quote_string(value)}' for key, value in self._get_items_list())
        return '{' + f'{d}' + '}'

    def __iter__(self) -> Iterator:
        return iter(self.keys())

    def __eq__(self, other: Mapping) -> bool:
        if not {'__len__', '__contains__', '__getitem__'}.issubset(dir(other)):
            return False
        if len(self) != len(other):
            return False
        for key in self.keys():
            if key not in other:
                return False
            if self[key] != other[key]:
                return False
        return True

    def __len__(self) -> int:
        return len(self._get_keys_list())

    def _get_values_list(self) -> list[Any]:
        return [self[key] for key in self._get_keys_list()]

    def _get_items_list(self) -> list[tuple]:
        return [(key, self[key]) for key in self._get_keys_list()]

    def copy(self):
        copy = self.__new__(type(self))
        copy.__init__(self._get_items_list())
        return copy

    def setdefault(self, key, default: Optional[Any] = None) -> Any:
        """Insert key with a value of default if key is not in the dictionary.

           Return the value for key if key is in the dictionary, else default.
        """
        if key not in self:
            self[key] = default
            return default
        return key

    def update(self, data: Optional[Iterable] = None) -> None:
        """Update self from dict/iterable data.
           If data is present and has a .keys() method, then does:  for k in data: self[k] = data[k]
           If data is present and lacks a .keys() method, then does:  for k, v in data: self[k] = v
        """
        if data is None:
            return
        if {'__setitem__', 'keys'}.issubset(dir(data)):
            for k in data._get_keys_list():
                self[k] = data[k]
        else:
            for k, v in data:
                self[k] = v