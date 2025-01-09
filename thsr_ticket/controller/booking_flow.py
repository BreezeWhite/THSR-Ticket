from requests.models import Response

from thsr_ticket.controller.confirm_train_flow import ConfirmTrainFlow
from thsr_ticket.controller.confirm_ticket_flow import ConfirmTicketFlow
from thsr_ticket.controller.first_page_flow import FirstPageFlow
from thsr_ticket.view_model.error_feedback import ErrorFeedback
from thsr_ticket.view_model.booking_result import BookingResult
from thsr_ticket.view.web.show_error_msg import ShowErrorMsg
from thsr_ticket.view.web.show_booking_result import ShowBookingResult
from thsr_ticket.view.common import history_info
from thsr_ticket.model.db import ParamDB
from thsr_ticket.remote.http_request import HTTPRequest


class BookingFlow:
    use_history = None
    record = None

    def __init__(self) -> None:
        self.client = HTTPRequest()
        self.db = ParamDB()
        self.error_feedback = ErrorFeedback()
        self.show_error_msg = ShowErrorMsg()

    def run(self) -> Response:
        if BookingFlow.use_history is None:
            self.show_history()

        # First page. Booking options
        book_resp, book_model, updated_record = FirstPageFlow(client=self.client, record=BookingFlow.record).run()
        if self.show_error(book_resp.content):
            return book_resp
        BookingFlow.record = updated_record

        # Second page. Train confirmation
        train_resp, train_model = ConfirmTrainFlow(self.client, book_resp, record=BookingFlow.record).run()
        if self.show_error(train_resp.content):
            return train_resp

        # Final page. Ticket confirmation
        ticket_resp, ticket_model = ConfirmTicketFlow(self.client, train_resp, BookingFlow.record).run()
        if self.show_error(ticket_resp.content):
            return ticket_resp

        # Result page.
        result_model = BookingResult().parse(ticket_resp.content)
        book = ShowBookingResult()
        book.show(result_model)
        print("\n請使用官方提供的管道完成後續付款以及取票!!")
        status = True
        return status

    def show_history(self) -> None:
        hist = self.db.get_history()
        if not hist:
            return
        h_idx = history_info(hist)
        if h_idx is not None:
            BookingFlow.use_history = True
            BookingFlow.record = hist[h_idx]
        else:
            BookingFlow.use_history = False
            BookingFlow.record = None

    def show_error(self, html: bytes) -> bool:
        errors = self.error_feedback.parse(html)
        if len(errors) == 0:
            return False

        self.show_error_msg.show(errors)
        return True
