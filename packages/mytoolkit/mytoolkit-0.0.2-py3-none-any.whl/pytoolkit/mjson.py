import json
from collections.abc import Mapping
from typing import Any, Union


def _is_basic_type(item: Any):
    if isinstance(item, (int, str, float, bool)):
        return True
    return False


class MJson(Mapping):
    def __init__(self, value: dict):
        self._value = value

    def __getitem__(self, key: Union[str, int, list[Union[int, str]]]):
        if isinstance(key, str):
            return self._value[key]

        t_value = self._value
        for k in key:
            t_value = t_value[k]
        if _is_basic_type(t_value):
            return t_value
        else:
            return MJson(t_value)

    def __iter__(self):
        for item in self._value:
            if _is_basic_type(item):
                yield item
            else:
                yield MJson(item)

    def __len__(self):
        return len(self._value)

    def __str__(self) -> str:
        return str(self._value)

    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def loads(cls, s, **kw) -> "MJson":
        value = json.loads(s, **kw)
        return MJson(value)
