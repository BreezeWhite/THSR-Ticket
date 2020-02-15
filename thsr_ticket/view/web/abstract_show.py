from typing import List, Any


class AbstractShow:
    def __init__(self) -> None:
        pass

    def show(self, items: List[Any], select: bool = False) -> int:
        raise NotImplementedError
