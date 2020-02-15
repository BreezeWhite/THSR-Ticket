from collections import namedtuple
from typing import Iterable

Code = namedtuple('Code', ['value', 'code'])


class BaseTicket:
    def __init__(self, keyword: str = "") -> None:
        self.combs = [Code(i, "{}{}".format(i, keyword)) for i in range(11)]

    def __iter__(self) -> Iterable[Code]:
        return iter(self.combs)

    def __len__(self) -> int:
        return len(self.combs)

    def get_code(self, val: int) -> str:
        for c in self.combs:
            if c.value == val:
                return c.code
        raise ValueError("Can't find corresponding code")


class AdultTicket(BaseTicket):
    def __init__(self) -> None:
        super(AdultTicket, self).__init__("F")


class ChildTicket(BaseTicket):
    def __init__(self) -> None:
        super(ChildTicket, self).__init__("H")


class DisabledTicket(BaseTicket):
    def __init__(self) -> None:
        super(DisabledTicket, self).__init__("W")


class ElderTicket(BaseTicket):
    def __init__(self) -> None:
        super(ElderTicket, self).__init__("E")


class CollegeTicket(BaseTicket):
    def __init__(self) -> None:
        super(CollegeTicket, self).__init__("P")
