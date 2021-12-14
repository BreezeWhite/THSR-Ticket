import io
from PIL import Image

from requests.models import Response
import matplotlib.pyplot as plt  # type: ignore
import numpy as np  # type: ignore
from bs4 import BeautifulSoup

from thsr_ticket.remote.http_request import HTTPRequest
from thsr_ticket.model.web.booking_form.booking_form import BookingForm
from thsr_ticket.model.web.booking_form.ticket_num import AdultTicket
from thsr_ticket.model.web.confirm_train import ConfirmTrain
from thsr_ticket.model.web.confirm_ticket import ConfirmTicket
from thsr_ticket.view_model.avail_trains import AvailTrains
from thsr_ticket.view_model.error_feedback import ErrorFeedback
from thsr_ticket.view_model.booking_result import BookingResult
from thsr_ticket.view.web.booking_form_info import BookingFormInfo
from thsr_ticket.view.web.show_avail_trains import ShowAvailTrains
from thsr_ticket.view.web.show_error_msg import ShowErrorMsg
from thsr_ticket.view.web.confirm_ticket_info import ConfirmTicketInfo
from thsr_ticket.view.web.show_booking_result import ShowBookingResult
from thsr_ticket.view.common import history_info
from thsr_ticket.model.db import ParamDB, Record
from thsr_ticket.configs.web.parse_html_element import BOOKING_PAGE, TICKET_CONFIRMATION


class BookingFlow:
    def __init__(self) -> None:
        self.client = HTTPRequest()

        self.book_form = BookingForm()
        self.book_info = BookingFormInfo()

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
        self.set_start_station()
        self.set_dest_station()
        self.book_form.outbound_date = self.book_info.date_info("出發")
        self.set_outbound_time()
        self.set_adult_ticket_num()
        print("等待驗證碼...")
        book_page = self.client.request_booking_page().content
        self.book_form.seat_prefer = parse_seat_prefer_value(book_page)
        self.book_form.security_code = self.input_security_code(book_page)

        form_params = self.book_form.get_params()
        result = self.client.submit_booking_form(form_params)
        if self.show_error(result.content):
            return result

        # Second page. Train confirmation
        avail_trains = AvailTrains().parse(result.content)
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
        self.confirm_ticket.id_radio_value = parse_person_id_radio_value(result)
        self.confirm_ticket.phone_radio_value = parse_mobile_radio_value(result)
        ticket_params = self.confirm_ticket.get_params()
        result = self.client.submit_ticket(ticket_params)
        if self.show_error(result.content):
            return result

        result_model = BookingResult().parse(result.content)
        book = ShowBookingResult()
        book.show(result_model)
        print("\n請使用官方提供的管道完成後續付款以及取票!!")

        self.db.save(self.book_form, self.confirm_ticket)
        return result

    def show_history(self) -> None:
        hist = self.db.get_history()
        h_idx = history_info(hist)
        if h_idx is not None:
            self.record = hist[h_idx]

    def set_start_station(self) -> None:
        if self.record.start_station is not None:
            self.book_form.start_station = self.record.start_station
        else:
            self.book_form.start_station = self.book_info.station_info("啟程")

    def set_dest_station(self) -> None:
        if self.record.dest_station is not None:
            self.book_form.dest_station = self.record.dest_station
        else:
            self.book_form.dest_station = self.book_form.dest_station = self.book_info.station_info("到達")

    def set_outbound_time(self) -> None:
        if self.record.outbound_time is not None:
            self.book_form.outbound_time = self.record.outbound_time
        else:
            self.book_form.outbound_time = self.book_info.time_table_info()

    def set_adult_ticket_num(self) -> None:
        if self.record.adult_num is not None:
            self.book_form.adult_ticket_num = self.record.adult_num
        else:
            sel = self.book_info.ticket_num_info("大人", default_value=1)
            self.book_form.adult_ticket_num = AdultTicket().get_code(sel)

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

    def input_security_code(self, book_page: bytes) -> str:
        img_resp = self.client.request_security_code_img(book_page)
        image = Image.open(io.BytesIO(img_resp.content))
        print("輸入驗證碼:")
        image.show()
        # img_arr = np.array(image)
        # plt.imshow(img_arr)
        # plt.show()
        return input()

    def show_error(self, html: bytes) -> bool:
        errors = self.error_feedback.parse(html)
        if len(errors) == 0:
            return False

        self.show_error_msg.show(errors)
        return True


def parse_seat_prefer_value(html: bytes) -> str:
    page = BeautifulSoup(html, features="html.parser")
    return page.find(**BOOKING_PAGE["seat_prefer_radio"]).attrs['value']


def parse_mobile_radio_value(html: bytes) -> str:
    page = BeautifulSoup(html, features="html.parser")
    return page.find(**TICKET_CONFIRMATION["mobile_input_radio"]).attrs['value']


def parse_person_id_radio_value(html: bytes) -> str:
    page = BeautifulSoup(html, features="html.parser")
    return page.find(**TICKET_CONFIRMATION["id_input_radio"]).attrs['value']
