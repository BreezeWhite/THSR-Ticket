from typing import Mapping, Any
from jsonschema import validate

from thsr_ticket.model.web.abstract_params import AbstractParams
from thsr_ticket.configs.web.param_schema import CONFIRM_TICKET_SHEMA


class ConfirmTicket(AbstractParams):
    def __init_(self) -> None:
        self._personal_id: str = None
        self._phone: str = ""

    def get_params(self, val: bool = True) -> Mapping[str, Any]:
        params = {
            "BookingS3FormSP:hf:0": "",
            "diffOver": 1,
            "idInputRadio": "radio36",
            "idInputRadio:idNumber": self._personal_id,
            "eaiPhoneCon:phoneInputRadio": "radio43",
            "eaiPhoneCon:phoneInputRadio:mobilePhone": self._phone,
            "email": "",
            "agree": "on",
            "isGoBackM": "",
            "backHome": "",
            "TgoError": "1"
        }

        if val:
            validate(params, schema=CONFIRM_TICKET_SHEMA)
        return params

    @property
    def personal_id(self) -> str:
        return self._personal_id

    @personal_id.setter
    def personal_id(self, value: str) -> None:
        if len(value) != 10:
            raise ValueError("Wrong length of R.O.C. ID. Should be 10, received {}".format(len(value)))
        self._personal_id = value

    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, value: str) -> None:
        if len(value) != 0 and len(value) != 10:
            raise ValueError("Wrong length of phone number. Should be 10, received {}".format(len(value)))
        if len(value) != 0 and not value.startswith("09"):
            raise ValueError("Wrong prefix with the phone number: {}".format(value))
        self._phone = value
