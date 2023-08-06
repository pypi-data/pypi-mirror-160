import json
from typing import List, Union


class _CustomerJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.__dict__


def _try_parse_int(value: str):
    try:
        return int(value)
    except ValueError:
        return value


class BJson:
    """
    BJson means blidz json, is a wrapper for json in python.
    Except the common function in json, also support find by path.
    Json包装，支持常见的查找，遍历等操作。
    json_str = '''{
    "a": {
     "b": {
       "c": 1
     },
     "list": [
          {
            "d": "2"
          },
          {
            "e": 3
          }
        ]
     }
    }'''
    1. 支持路径查找: 例如查找中c的值，可以直接BJson.loads(json_str)["a/b/c"]
    2. 支持路径中包含下标方式的查找: 例如查找e的值，可以直接BJson.loads(json_str)["a/list/1/e"]
    3. 迭代: list(BJson.loads(json_str)["a/list"])
    """

    def __init__(self, json_obj):
        self._value = json_obj

    def __contains__(self, path: List[Union[int, str]]):
        if not isinstance(path, list):
            raise TypeError(f'path must be a list, got {type(path).__name__}')
        current_json = self._value
        for p in path:
            try:
                current_json = current_json[p]
            except KeyError:
                return False
            except TypeError:
                return False
            except IndexError:
                return False
        return True

    def __iter__(self):
        for item in self._value:
            if isinstance(item, int) or isinstance(item, str) or isinstance(item, float):
                yield item
            else:
                yield BJson(item)

    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return repr(self._value)

    def __getitem__(self, path: Union[List[Union[int, str]], str, int]):
        if isinstance(path, str) or isinstance(path, int):
            path = [path]
        if not isinstance(path, list):
            raise TypeError(f'path must be a list, got {type(path).__name__}')
        current_json = self._value
        for p in path:
            current_json = current_json[p]
        if isinstance(current_json, int) or isinstance(current_json, str) or isinstance(current_json, float):
            return current_json
        return BJson(current_json)

    def __eq__(self, other):
        return repr(self._value) == repr(other)

    def __len__(self):
        return len(self._value)

    def __bool__(self):
        return bool(self._value)

    def __setitem__(self, key, value):
        if not hasattr(self._value, "__setitem__"):
            raise TypeError(
                '%s object does not support item assignment' % type(self._value).__name__)
        self._value[key] = value

    @property
    def value(self):
        return self._value

    def _find_by_path(self, path: List[Union[int, str]],):
        if not isinstance(path, list):
            raise TypeError(f'path must be a list, got {type(path).__name__}')
        current_json = self._value
        for p in path:
            try:
                current_json = current_json[p]
            except KeyError:
                return None
            except TypeError:
                return None
            except IndexError:
                return None
        return current_json

    def get(self, path: Union[List[Union[int, str]], str, int], default=None):
        try:
            return self.__getitem__(path)
        except KeyError:
            return default
        except IndexError:
            return default
        except TypeError:
            return default

    def get_value(self, path: Union[List[Union[int, str]], str, int], default=None):
        try:
            result = self.__getitem__(path)
            if isinstance(result, BJson):
                return result.value
            return result
        except KeyError:
            return default
        except IndexError:
            return default
        except TypeError:
            return default

    def find_value(self, path: Union[List[Union[int, str]], str, int], expected_value: Union[int, float, str]) -> bool:
        pass

    @staticmethod
    def dumps(obj):
        return json.dumps(obj, cls=_CustomerJSONEncoder)

    @classmethod
    def loads(cls, json_str, **kwargs):
        if not json_str:
            return None
        t_json = json.loads(json_str, **kwargs)
        return BJson(t_json)


if __name__ == "__main__":
    json_str = '''
    {
    "a":"a",
    "b":{
        "bb":1
    },
    "list":[
        {
            "c1":"c1"
        },
        {
            "c2":2.9
        }
    ]
    }'''
    bjson = BJson.loads(json_str)
    # print(bjson)
    print(bjson["a"])
    print(bjson["b"])
    print(bjson["list"])
    for node in bjson["list"]:
        print(node)
