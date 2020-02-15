from typing import Any
import datetime

from thsr_ticket.configs.common import DAYS_BEFORE_BOOKING_AVAILABLE
from thsr_ticket.model.web.booking_form.station_mapping import StationMapping
from thsr_ticket.model.web.booking_form.ticket_num import BaseTicket
from thsr_ticket.model.web.booking_form.time_table import TimeTable


class BookingFormInfo:
    def __init__(self) -> None:
        self.station_mapping: Any = StationMapping
        self.time_table: Any = TimeTable()

    def station_info(self, station_type: str, default_value: int = None, select: bool = True) -> int:
        print("選擇{}站: ".format(station_type))
        for station in self.station_mapping:
            print("{}. {}".format(station.value, station.name))

        if select:
            return int(input("輸入選擇(預設: {}): ".format(str(default_value))) or default_value)
        return None

    def date_info(self, date_type: str, select: bool = True) -> str:
        today = datetime.datetime.now()
        avail_day = today + datetime.timedelta(days=DAYS_BEFORE_BOOKING_AVAILABLE)
        fmt = "%Y/%m/%d"
        print("選擇{}日期 ({}~{}) (預設為今日):".format(
            date_type, today.strftime(fmt), avail_day.strftime(fmt)
        ))
        if select:
            return input() or today.strftime(fmt)
        return None

    def ticket_num_info(self, ticket_type: str, default_value: int = 0, select: bool = True) -> int:
        max_num = len(BaseTicket()) - 1
        print("選擇{}票數 ({}~{}) (預設: {}): ".format(0, ticket_type, max_num, default_value))
        if select:
            return int(input() or default_value)
        return None

    def time_table_info(self, default_value: int = None, select: bool = True) -> str:
        print("選擇出發時間:")
        for t in self.time_table:
            t_int = int(t.time[:-1])
            if t.time[-1] == "A" and (t_int // 100) == 12:
                t_int = "{:04d}".format(t_int % 1200)  # type: ignore
            elif t_int != 1230 and t.time[-1] == "P":
                t_int += 1200
            t_str = str(t_int)
            print("{}. {}:{}".format(t.value, t_str[:-2], t_str[-2:]))

        if select:
            return self.time_table.get_time(
                int(input("輸入選擇(預設: {}): ".format(default_value)) or default_value)
            )
        return None
