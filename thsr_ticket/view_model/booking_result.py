from typing import List, Mapping, Any
from collections import namedtuple

from bs4 import BeautifulSoup

from thsr_ticket.view_model.abstract_view_model import AbstractViewModel
from thsr_ticket.configs.web.parse_html_element import BOOKING_RESULT

Ticket = namedtuple("Ticket", [
        "id", "price", "start_station", "dest_station", "train_id", "depart_time", "arrival_time",
        "date", "seat", "seat_class", "payment_deadline", "ticket_num_info"
])


class BookingResult(AbstractViewModel):
    def __init__(self) -> None:
        super(BookingResult, self).__init__()
        self.ticket: Ticket = None

    def parse(self, html: bytes) -> List[Ticket]:
        page = self._parser(html)
        ticket = page.find(**BOOKING_RESULT["ticket_id"])
        booking_id = ticket.find_next().text
        deadline = page.find(**BOOKING_RESULT["payment_deadline"]).find_next().text
        outbound_info = self.parse_booking_info(page)
        seat_class = page.find(**BOOKING_RESULT["seat_class"]).text
        ticket_num_info = self.parse_ticket_num(page)
        self.ticket = Ticket(
            id=booking_id,
            payment_deadline=deadline,
            seat_class=seat_class,
            ticket_num_info=ticket_num_info,
            **outbound_info
        )
        return [self.ticket]

    def parse_booking_info(self, page: BeautifulSoup) -> Mapping[str, Any]:
        table = page.find(**BOOKING_RESULT["info"])
        outbound = table.find(**BOOKING_RESULT["outbound_info"])
        outbound_info = {}
        for key in BOOKING_RESULT["info_order"]:
            outbound = outbound.find_next("span")
            outbound_info[key] = outbound.text
        rest_seat = outbound.find_next_siblings()
        seat_str = "".join([outbound_info[key]]+[s.text for s in rest_seat])
        outbound_info[key] = seat_str

        return outbound_info

    def parse_ticket_num(self, page: BeautifulSoup) -> str:
        tags = page.find(**BOOKING_RESULT["ticket_num"]).find_next_siblings()
        return "|".join([t.text for t in tags])
