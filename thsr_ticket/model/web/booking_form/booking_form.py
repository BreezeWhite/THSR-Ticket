from datetime import datetime, timedelta
from typing import Mapping, Any

from jsonschema import validate

from thsr_ticket.model.web.abstract_params import AbstractParams
from thsr_ticket.configs.web.param_schema import BOOKING_SCHEMA


class BookingForm(AbstractParams):
    def __init__(self) -> None:
        """
        Station number mapping:
            1: Nangang
            2: Taipei
            3: Banqiao
            4: Taoyuan
            5: Hsinchu
            6: Miaoli
            7: Taichung
            8: Changhua
            9: Yunlin
            10: Chiayi
            11: Tainan
            12: Zuoying
        """
        super(BookingForm, self).__init__()
        self._start_station: int = None  # Required
        self._dest_station: int = None  # Required
        self._class_type: int = 0
        self._seat_prefer: str = "radio17"
        self._search_by: int = 0
        self._outbound_date: str = None  # Required
        self._outbound_time: str = None  # Required
        self._inbound_date: str = ""
        self._inbound_time: str = ""
        self._adult_ticket_num: str = "1F"
        self._child_ticket_num: str = "0H"
        self._disabled_ticket_num: str = "0W"
        self._elder_ticket_num: str = "0E"
        self._college_ticket_num: str = "0P"
        self.security_code: str = None  # Required

    def get_params(self, val: bool = True) -> Mapping[str, Any]:
        if self._inbound_date is None:
            self._inbound_date = self.outbound_date
        params = {
            "BookingS1Form:hf:0": "",
            "selectStartStation": self._start_station,
            "selectDestinationStation": self._dest_station,
            "trainCon:trainRadioGroup": self._class_type,
            "seatCon:seatRadioGroup": self._seat_prefer,
            "bookingMethod": self._search_by,
            "toTimeInputField": self._outbound_date,
            "toTimeTable": self._outbound_time,
            "toTrainIDInputField": 0,
            "backTimeInputField": self._inbound_date,
            "backTimeTable": self._inbound_time,
            "backTrainIDInputField": "",
            "ticketPanel:rows:0:ticketAmount": self._adult_ticket_num,
            "ticketPanel:rows:1:ticketAmount": self._child_ticket_num,
            "ticketPanel:rows:2:ticketAmount": self._disabled_ticket_num,
            "ticketPanel:rows:3:ticketAmount": self._elder_ticket_num,
            "ticketPanel:rows:4:ticketAmount": self._college_ticket_num,
            "homeCaptcha:securityCode": self.security_code
        }

        if val:
            validate(params, schema=BOOKING_SCHEMA)
        return params

    @property
    def start_station(self) -> int:
        return self._start_station

    @start_station.setter
    def start_station(self, value: int) -> None:
        self._validate_value("selectStartStation", value)
        self._start_station = value

    @property
    def dest_station(self) -> int:
        return self._dest_station

    @dest_station.setter
    def dest_station(self, value: int) -> None:
        self._validate_value("selectDestinationStation", value)
        self._dest_station = value

    @property
    def class_type(self) -> int:
        return self._class_type

    @class_type.setter
    def class_type(self, value: int) -> None:
        self._validate_value("trainCon:trainRadioGroup", value)
        self._class_type = value

    @property
    def seat_prefer(self) -> str:
        return self._seat_prefer

    @seat_prefer.setter
    def seat_prefer(self, value: str) -> None:
        self._validate_value("seatCon:seatRadioGroup", value)
        self._seat_prefer = value

    @property
    def search_by(self) -> int:
        return self._search_by

    @search_by.setter
    def search_by(self, value: int) -> None:
        self._validate_value("bookingMethod", value)
        self._search_by = value

    @property
    def outbound_date(self) -> str:
        return self._outbound_date

    @outbound_date.setter
    def outbound_date(self, value: str) -> None:
        date = self._validate_date(value)
        if (date-datetime.now()) < timedelta(seconds=60):
            raise ValueError("Departure date should not be earlier than today")
        self._outbound_date = value

    @property
    def outbound_time(self) -> str:
        return self._outbound_time

    @outbound_time.setter
    def outbound_time(self, value: str) -> None:
        self._validate_value("toTimeTable", value)
        self._outbound_time = value

    @property
    def inbound_date(self) -> str:
        return self._inbound_date

    @inbound_date.setter
    def inbound_date(self, value: str) -> None:
        in_date = self._validate_date(value)
        if self._outbound_date is not None:
            out_date = datetime.strptime(self._outbound_date, '%Y/%m/%d')
            if out_date > in_date:
                raise ValueError("Inbound date shouldn't be earlier than outbound date!")

        self._inbound_date = value

    @property
    def inbound_time(self) -> str:
        return self._inbound_time

    @inbound_time.setter
    def inbound_time(self, value: str) -> None:
        self._validate_value("backTimeTable", value)
        self._inbound_time = value

    @property
    def adult_ticket_num(self) -> str:
        return self._adult_ticket_num

    @adult_ticket_num.setter
    def adult_ticket_num(self, value: str) -> None:
        self._validate_value("ticketPanel:rows:0:ticketAmount", value)
        self._adult_ticket_num = value

    @property
    def child_ticket_num(self) -> str:
        return self._child_ticket_num

    @child_ticket_num.setter
    def child_ticket_num(self, value: str) -> None:
        self._validate_value("ticketPanel:rows:1:ticketAmount", value)
        self._child_ticket_num = value

    @property
    def disabled_ticket_num(self) -> str:
        return self._disabled_ticket_num

    @disabled_ticket_num.setter
    def disabled_ticket_num(self, value: str) -> None:
        self._validate_value("ticketPanel:rows:2:ticketAmount", value)
        self._disabled_ticket_num = value

    @property
    def elder_ticket_num(self) -> str:
        return self._elder_ticket_num

    @elder_ticket_num.setter
    def elder_ticket_num(self, value: str) -> None:
        self._validate_value("ticketPanel:rows:3:ticketAmount", value)
        self._elder_ticket_num = value

    @property
    def college_ticket_num(self) -> str:
        return self._college_ticket_num

    @college_ticket_num.setter
    def college_ticket_num(self, value: str) -> None:
        self._validate_value("ticketPanel:rows:4:ticketAmount", value)
        self._college_ticket_num = value

    def _validate_date(self, value: Any) -> datetime:
        return datetime.strptime(value, '%Y/%m/%d')

    def _validate_value(self, proper: str, value: Any) -> None:
        if value not in BOOKING_SCHEMA["properties"][proper]["enum"]:
            raise ValueError("Value '{}' is not allowed for this attribute '{}'".format(value, proper))
