from typing import Mapping, Any


BOOKING_PAGE: Mapping[str, Any] = {
    "security_code_img": {
        "id": "BookingS1Form_homeCaptcha_passCode"
    }
}

ERROR_FEEDBACK: Mapping[str, Any] = {
    "name": "span",
    "attrs": {
        "class": "feedbackPanelERROR"
    }
}

BOOKING_RESULT: Mapping[str, Any] = {
    "ticket_id": {
        "text": "訂位代號"
    },
    "payment_deadline": {
        "text": "（付款期限："
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
    "info_order": [
        "date", "train_id", "start_station", "dest_station", "depart_time", 
        "arrival_time", "price", "seat"
    ],
    "seat_class": {
        "name": "span",
        "attrs": {
            "class": "PR20"
        }
    },
    "ticket_num": {
        "name": "strong",
        "text": "票數："
    }
}
