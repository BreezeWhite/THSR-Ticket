import io
from PIL import Image

from requests.models import Response
from bs4 import BeautifulSoup
from thsr_ticket.controller.first_page_flow import FirstPageFlow

from thsr_ticket.remote.http_request import HTTPRequest
from thsr_ticket.model.web.confirm_train import ConfirmTrain
from thsr_ticket.model.web.confirm_ticket import ConfirmTicket
from thsr_ticket.view_model.avail_trains import AvailTrains
from thsr_ticket.view_model.error_feedback import ErrorFeedback
from thsr_ticket.view_model.booking_result import BookingResult
from thsr_ticket.view.web.show_avail_trains import ShowAvailTrains
from thsr_ticket.view.web.show_error_msg import ShowErrorMsg
from thsr_ticket.view.web.confirm_ticket_info import ConfirmTicketInfo
from thsr_ticket.view.web.show_booking_result import ShowBookingResult
from thsr_ticket.view.common import history_info
from thsr_ticket.model.db import ParamDB, Record


class BookingFlow:
    def __init__(self) -> None:
        self.client = HTTPRequest()

        self.confirm_train = ConfirmTrain()
        self.show_avail_trains = ShowAvailTrains()

        self.confirm_ticket = ConfirmTicket()
        self.confirm_ticket_info = ConfirmTicketInfo()

        self.error_feedback = ErrorFeedback()
        self.show_error_msg = ShowErrorMsg()

        self.db = ParamDB()
        self.record = Record()

    def run(self) -> Response:
        self.show_history()

        # First page. Booking options
        book_resp, book_model = FirstPageFlow(client=self.client, record=self.record).run()
        if self.show_error(book_resp.content):
            return book_resp

        # Second page. Train confirmation
        avail_trains = AvailTrains().parse(book_resp.content)
        sel = self.show_avail_trains.show(avail_trains)
        value = avail_trains[sel-1].form_value  # Selection from UI count from 1
        self.confirm_train.selection = value
        confirm_params = self.confirm_train.get_params()
        result = self.client.submit_train(confirm_params).content
        if self.show_error(result):
            return result

        # Third page. Ticket confirmation
        self.set_personal_id()
        self.set_phone()
        page = BeautifulSoup(result, features="html.parser")
        self.confirm_ticket.member_radio = parse_member_radio(page)
        ticket_params = self.confirm_ticket.get_params()
        result = self.client.submit_ticket(ticket_params)
        if self.show_error(result.content):
            return result

        result_model = BookingResult().parse(result.content)
        book = ShowBookingResult()
        book.show(result_model)
        print("\n請使用官方提供的管道完成後續付款以及取票!!")

        self.db.save(book_model, self.confirm_ticket)
        return result

    def show_history(self) -> None:
        hist = self.db.get_history()
        if not hist:
            return
        h_idx = history_info(hist)
        if h_idx is not None:
            self.record = hist[h_idx]

    def set_personal_id(self) -> None:
        if self.record.personal_id is not None:
            self.confirm_ticket.personal_id = self.record.personal_id
        else:
            self.confirm_ticket.personal_id = self.confirm_ticket_info.personal_id_info()

    def set_phone(self) -> None:
        if self.record.phone is not None:
            self.confirm_ticket.phone = self.record.phone
        else:
            self.confirm_ticket.phone = self.confirm_ticket_info.phone_info()

    def show_error(self, html: bytes) -> bool:
        errors = self.error_feedback.parse(html)
        if len(errors) == 0:
            return False

        self.show_error_msg.show(errors)
        return True


def parse_member_radio(page: BeautifulSoup) -> str:
    candidates = page.find_all(
        'input',
        attrs={
            'name': 'TicketMemberSystemInputPanel:TakerMemberSystemDataView:memberSystemRadioGroup'
        },
    )
    tag = next((cand for cand in candidates if 'checked' in cand.attrs))
    return tag.attrs['value']
