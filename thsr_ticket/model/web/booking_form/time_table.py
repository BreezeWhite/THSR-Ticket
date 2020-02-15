from collections import namedtuple
from typing import Iterable

from thsr_ticket.configs.web.param_schema import BOOKING_SCHEMA

Table = namedtuple('Table', ['value', 'time'])


class TimeTable:
    def __init__(self) -> None:
        self.table = []
        for idx, t in enumerate(BOOKING_SCHEMA["properties"]["toTimeTable"]["enum"], 1):
            self.table.append(Table(idx, t))

    def __iter__(self) -> Iterable[Table]:
        return iter(self.table)

    def __len__(self) -> int:
        return len(self.table)

    def get_time(self, val: int) -> str:
        for t in self.table:
            if t.value == val:
                return t.time
        raise ValueError("Can't find corresponding time")
