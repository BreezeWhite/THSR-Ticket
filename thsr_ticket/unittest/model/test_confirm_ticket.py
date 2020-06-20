import pytest

from thsr_ticket.model.web.confirm_ticket import ConfirmTicket

ticket = ConfirmTicket()


@pytest.mark.parametrize("val", ["tooshort", "toooooooooolong"])
def test_set_id(val):
    with pytest.raises(ValueError):
        ticket.personal_id = val


@pytest.mark.parametrize("val,err_msg", [
    ("0812345667", "Wrong prefix"),
    ("0911244", "Wrong length")
])
def test_phone(val, err_msg):
    with pytest.raises(ValueError) as exc_info:
        ticket.phone = val
    assert err_msg in str(exc_info.value)
    ticket.phone = "0945789123"
    assert ticket.phone == "0945789123"


def test_get_params():
    expected = {
        "BookingS3FormSP:hf:0": "",
        "diffOver": 1,
        "idInputRadio": "radio36",
        "idInputRadio:idNumber": "A186902624",
        "eaiPhoneCon:phoneInputRadio": "radio43",
        "eaiPhoneCon:phoneInputRadio:mobilePhone": "0945789123",
        "email": "",
        "agree": "on",
        "isGoBackM": "",
        "backHome": "",
        "TgoError": "1"
    }

    with pytest.raises(AttributeError):
        ticket.get_params()

    ticket.personal_id = "A186902624"
    assert ticket.personal_id == "A186902624"
    assert ticket.get_params() == expected
