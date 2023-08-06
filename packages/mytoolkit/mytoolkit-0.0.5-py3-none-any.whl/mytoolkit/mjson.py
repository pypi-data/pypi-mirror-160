import json
from collections.abc import Mapping
from typing import Any, List, Union
import sys

def _is_basic_type(item: Any):
    if isinstance(item, (int, str, float, bool)):
        return True
    return False


class MJson(Mapping):
    def __init__(self, value: dict):
        self._value = value

    def __getitem__(self, key: Union[str, int, List[Union[int, str]]]):
        if isinstance(key, str):
            t_value = self._value[key]
        else:
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

    @property
    def value(self):
        return self._value

    @classmethod
    def loads(cls, s, **kw) -> "MJson":
        value = json.loads(s, **kw)
        return MJson(value)

    def get(self, key: Union[str, int, List[Union[int, str]]], default: Any = None):
        try:
            return self.__getitem__(key)
        except (KeyError, IndexError):
            return default

    def find_by_key(self, key: str, count: int = -1):
        if count <=0:
            count = sys.maxsize
        res = []
        temp_nodes = [self]
        while temp_nodes:
            node = temp_nodes.pop(0)
            if isinstance(node.value, dict):
                for k, v in node.items():
                    if k == key:
                        res.append(v)
                        if len(res) == count:
                            return res
                    if not _is_basic_type(v):
                        temp_nodes.append(v)
            elif isinstance(node.value, list):
                for v in node:
                    if not _is_basic_type(v):
                        temp_nodes.append(v)
        return res

    def find_one_by_key(self, key: str):
        res = self.find_by_key(key, 1)
        if res:
            return res[0]
        return None

json_str = """
{
    "products":[
        {
            "id":1,
            "title":"iPhone 9",
            "description":"An apple mobile which is nothing like apple",
            "price":549,
            "discountPercentage":12.96,
            "rating":4.69,
            "stock":94,
            "brand":"Apple",
            "category":"smartphones",
            "thumbnail":"https://dummyjson.com/image/i/products/1/thumbnail.jpg",
            "images":[
                "https://dummyjson.com/image/i/products/1/1.jpg",
                "https://dummyjson.com/image/i/products/1/2.jpg",
                "https://dummyjson.com/image/i/products/1/3.jpg",
                "https://dummyjson.com/image/i/products/1/4.jpg",
                "https://dummyjson.com/image/i/products/1/thumbnail.jpg"
            ]
        },
        {
            "id":2,
            "title":"iPhone X",
            "description":"SIM-Free, Model A19211 6.5-inch Super Retina HD display with OLED technology ...",
            "price":899,
            "discountPercentage":17.94,
            "rating":4.44,
            "stock":34,
            "brand":"Apple",
            "category":"smartphones",
            "thumbnail":"https://dummyjson.com/image/i/products/2/thumbnail.jpg",
            "images":[
                "https://dummyjson.com/image/i/products/2/1.jpg",
                "https://dummyjson.com/image/i/products/2/2.jpg",
                "https://dummyjson.com/image/i/products/2/3.jpg",
                "https://dummyjson.com/image/i/products/2/thumbnail.jpg"
            ]
        },
        {
            "id":3,
            "title":"Samsung Universe 9",
            "description":"Samsung's new variant which goes beyond Galaxy to the Universe",
            "price":1249,
            "discountPercentage":15.46,
            "rating":4.09,
            "stock":36,
            "brand":"Samsung",
            "category":"smartphones",
            "thumbnail":"https://dummyjson.com/image/i/products/3/thumbnail.jpg",
            "images":[
                "https://dummyjson.com/image/i/products/3/1.jpg"
            ]
        },
        {
            "id":4,
            "title":"OPPOF19",
            "description":"OPPO F19 is officially announced on April 2021.",
            "price":280,
            "discountPercentage":17.91,
            "rating":4.3,
            "stock":123,
            "brand":"OPPO",
            "category":"smartphones",
            "thumbnail":"https://dummyjson.com/image/i/products/4/thumbnail.jpg",
            "images":[
                "https://dummyjson.com/image/i/products/4/1.jpg",
                "https://dummyjson.com/image/i/products/4/2.jpg",
                "https://dummyjson.com/image/i/products/4/3.jpg",
                "https://dummyjson.com/image/i/products/4/4.jpg",
                "https://dummyjson.com/image/i/products/4/thumbnail.jpg"
            ]
        },
        {
            "id":5,
            "title":"Huawei P30",
            "description":"Huawei’s re-badged P30 Pro New Edition was officially unveiled yesterday in Germany ...",
            "price":499,
            "discountPercentage":10.58,
            "rating":4.09,
            "stock":32,
            "brand":"Huawei",
            "category":"smartphones",
            "thumbnail":"https://dummyjson.com/image/i/products/5/thumbnail.jpg",
            "images":[
                "https://dummyjson.com/image/i/products/5/1.jpg",
                "https://dummyjson.com/image/i/products/5/2.jpg",
                "https://dummyjson.com/image/i/products/5/3.jpg"
            ]
        }
    ],
    "total":100,
    "skip":0,
    "limit":5
}
"""

if __name__ == '__main__':
    value = MJson.loads(json_str)
    print(value.find_one_by_key("id"))