import json
from typing import Any


class BaseResponse:
    def __init__(self) -> None:
        pass

    def to_json(self) -> str:
        # Returns: json string
        # To get python object, use json.loads(json_str) externally
        return json.dumps(self, default=lambda o: o.__dict__)

    def from_json(self, in_data: str) -> Any:  # noqa: F821
        data = json.loads(in_data)
        for k in self.__dict__.keys():
            if isinstance(data[k], list):
                instance = self.__dict__[k][0]
                instance_list = [instance.from_json(obj) for obj in data[k]]
                self.__dict__[k] = instance_list
            elif isinstance(data[k], dict) and k != "Note":
                self.__dict__[k] = self.__dict__[k].from_json(data[k])
            else:
                self.__dict__[k] = data[k]
        return self
