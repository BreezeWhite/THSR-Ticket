from typing import Mapping, Any


class AbstractParams:
    def __init__(self) -> None:
        pass

    def get_params(self, val: bool = True) -> Mapping[str, Any]:
        raise NotImplementedError
