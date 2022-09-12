from typing import Mapping, Any


BOOKING_PAGE: Mapping[str, Any] = {
    "security_code_img": {
        "id": "BookingS1Form_homeCaptcha_passCode"
    },
    "seat_prefer_radio": {
        "id": "BookingS1Form_seatCon_seatRadioGroup"
    },
    "types_of_trip": {
        "id": "BookingS1Form_tripCon_typesoftrip"
    }
}

ERROR_FEEDBACK: Mapping[str, Any] = {
    "name": "span",
    "attrs": {
        "class": "feedbackPanelERROR"
    }
}

TICKET_CONFIRMATION: Mapping[str, Any] = {
    "id_input_radio": {
        "id": "idInputRadio1"
    },
    "mobile_input_radio": {
        "id": "mobileInputRadio"
    }
}

BOOKING_RESULT: Mapping[str, Any] = {
    "ticket_id": {
        "name": "p",
        "attrs": {"class": "pnr-code"}
    },
    "payment_deadline": {
        "name": "p",
        "attrs": {"class": "payment-status"}
    },
    "phone": {
        "text": "行動電話"
    },
    "info": {
        "name": "table",
        "attrs": {
            "class": "table_simple"
        }
    },
    "outbound_info": {
        "text": "去程"
    },
    "seat_class": {
        "text": "車廂",
    },
    "ticket_num": {
        "name": "p",
        "text": "票數"
    },
    "total_price": {
        "id": "setTrainTotalPriceValue"
    },
    "train_id": {
        "id": "setTrainCode0"
    },
    "depart_time": {
        "id": "setTrainDeparture0"
    },
    "arrival_time": {
        "id": "setTrainArrival0"
    },
    "seat_num": {
        "name": "div",
        "attrs": {
            "class": "seat-label"
        }
    },
    "depart_station": {
        "name": "p",
        "attrs": {
            "class": "departure-stn"
        }
    },
    "arrival_station": {
        "name": "p",
        "attrs": {
            "class": "arrival-stn"
        }
    },
    "date": {
        "name": "span",
        "attrs": {"class": "date"}
    }
}
