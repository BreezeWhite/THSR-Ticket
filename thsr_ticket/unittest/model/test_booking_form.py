import pytest
import datetime
import jsonschema

from thsr_ticket.model.web.booking_form.booking_form import BookingForm

book = BookingForm()


@pytest.fixture
def tomorrow():
    tom = datetime.datetime.today() + datetime.timedelta(days=1)
    return tom.strftime("%Y/%m/%d")


@pytest.mark.parametrize("val", [0, 5.5, 13])
def test_set_station(val):
    with pytest.raises(ValueError):
        book.start_station = val
    book.start_station = 2
    assert book.start_station == 2

    with pytest.raises(ValueError):
        book.dest_station = val
    book.dest_station = 9
    assert book.dest_station == 9


@pytest.mark.parametrize("val", [0.5, 2])
def test_class_type(val):
    with pytest.raises(ValueError):
        book.class_type = val
    book.class_type = 0
    assert book.class_type == 0


@pytest.mark.parametrize("val", ["radio16", "ohoh"])
def test_seat_prefer(val):
    with pytest.raises(ValueError):
        book.seat_prefer = val
    book.seat_prefer = "radio17"
    assert book.seat_prefer == "radio17"


@pytest.mark.parametrize("val", ["2, 0.5"])
def test_search_by(val):
    with pytest.raises(ValueError):
        book.search_by = val
    book.search_by = 0
    assert book.search_by == 0


@pytest.mark.parametrize("val", [
    "1990/01/15", "20200202", "2020-01-01", "2020/1/3"
])
def test_outbound_date(val, tomorrow):
    with pytest.raises(ValueError):
        book.outbound_date = val
    book.outbound_date = tomorrow
    assert book.outbound_date == tomorrow


@pytest.mark.parametrize("val", ["123A", "1000B"])
def test_time(val):
    with pytest.raises(ValueError):
        book.outbound_time = val
    with pytest.raises(ValueError):
        book.inbound_time = val

    book.outbound_time = "530P"
    assert book.outbound_time == "530P"


@pytest.mark.parametrize("val", ["2001/07/08", "12345678"])
def test_inbound_date(val, tomorrow):
    with pytest.raises(ValueError):
        book.inbound_date = val
    book.inbound_date = tomorrow
    assert book.inbound_date == tomorrow


@pytest.mark.parametrize("val", ["11F", "5.5F", "8B"])
def test_ticket_num(val):
    with pytest.raises(ValueError):
        book.adult_ticket_num = val
    book.adult_ticket_num = "1F"
    assert book.adult_ticket_num == "1F"

    with pytest.raises(ValueError):
        book.child_ticket_num = val
    book.child_ticket_num = "0H"
    assert book.child_ticket_num == "0H"

    with pytest.raises(ValueError):
        book.disabled_ticket_num = val
    book.disabled_ticket_num = "0W"
    assert book.disabled_ticket_num == "0W"

    with pytest.raises(ValueError):
        book.elder_ticket_num = val
    book.elder_ticket_num = "0E"
    assert book.elder_ticket_num == "0E"

    with pytest.raises(ValueError):
        book.college_ticket_num = val
    book.college_ticket_num = "0P"
    assert book.college_ticket_num == "0P"


def test_get_params(tomorrow):
    captcha = "2A1B"
    expected = {
        "BookingS1Form:hf:0": "",
        "selectStartStation": 2,
        "selectDestinationStation": 9,
        "trainCon:trainRadioGroup": 0,
        "seatCon:seatRadioGroup": "radio17",
        "bookingMethod": 0,
        "toTimeInputField": tomorrow,
        "toTimeTable": "530P",
        "toTrainIDInputField": 0,
        "backTimeInputField": tomorrow,
        "backTimeTable": "",
        "backTrainIDInputField": "",
        "ticketPanel:rows:0:ticketAmount": "1F",
        "ticketPanel:rows:1:ticketAmount": "0H",
        "ticketPanel:rows:2:ticketAmount": "0W",
        "ticketPanel:rows:3:ticketAmount": "0E",
        "ticketPanel:rows:4:ticketAmount": "0P",
        "homeCaptcha:securityCode": captcha
    }

    with pytest.raises(jsonschema.exceptions.ValidationError):
        book.get_params()
    book.security_code = captcha
    assert book.get_params() == expected
