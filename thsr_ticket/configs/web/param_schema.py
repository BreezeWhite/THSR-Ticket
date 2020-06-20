from typing import Mapping, Any

BOOKING_SCHEMA: Mapping[str, Any] = {
    "type": "object",
    "properties": {
        "BookingS1Form:hf:0": {"type": "string"},
        "selectStartStation": {
            "type": "integer",
            "enum": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        },
        "selectDestinationStation": {
            "type": "integer",
            "enum": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        },
        "trainCon:trainRadioGroup": {
            "type": "integer",  # Class
            "enum": [0, 1]  # Standard car / Business car
        },
        "seatCon:seatRadioGroup": {
            "type": "string",  # Seat perference
            "enum": ["radio17", "radio19", "radio21"]  # None / Window seat / Aisle seat
        },
        "bookingMethod": {
            "type": "integer",  # Search seat by...
            "enum": [0, 1]  # Depart,Arrival time / Train No.
        },
        "toTimeInputField": {"type": "string"},  # format: yyyy/mm/dd
        "toTimeTable": {
            "type": "string",
            "enum": [
                "1201A", "1230A", "600A", "630A", "700A", "730A", "800A", "830A", "900A",
                "930A", "1000A", "1030A", "1100A", "1130A", "1200N", "1230P", "100P", "130P",
                "200P", "230P", "300P", "330P", "400P", "430P", "500P", "530P", "600P",
                "630P", "700P", "730P", "800P", "830P", "900P", "930P", "1000P", "1030P",
                "1100P", "1130P"
            ]
        },
        "toTrainIDInputField": {"type": "integer"},
        "backTimeInputField": {"type": "string"},
        "backTimeTable": {
            "type": "string",
            "enum": [
                "1201A", "1230A", "600A", "630A", "700A", "730A", "800A", "830A", "900A",
                "930A", "1000A", "1030A", "1100A", "1130A", "1200N", "1230P", "100P", "130P",
                "200P", "230P", "300P", "330P", "400P", "430P", "500P", "530P", "600P",
                "630P", "700P", "730P", "800P", "830P", "900P", "930P", "1000P", "1030P",
                "1100P", "1130P", ""
            ]
        },
        "backTrainIDInputField": {"type": "string"},
        "ticketPanel:rows:0:ticketAmount": {
            "type": "string",  # Adult ticket
            "enum": ["0F", "1F", "2F", "3F", "4F", "5F", "6F", "7F", "8F", "9F", "10F"]
        },
        "ticketPanel:rows:1:ticketAmount": {
            "type": "string",  # Child ticket (6~11)
            "enum": ["0H", "1H", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H"]
        },
        "ticketPanel:rows:2:ticketAmount": {
            "type": "string",  # Disabled ticket (Taiwan only)
            "enum": ["0W", "1W", "2W", "3W", "4W", "5W", "6W", "7W", "8W", "9W", "10W"]
        },
        "ticketPanel:rows:3:ticketAmount": {
            "type": "string",  # Elder ticket (Taiwan only)
            "enum": ["0E", "1E", "2E", "3E", "4E", "5E", "6E", "7E", "8E", "9E", "10E"]
        },
        "ticketPanel:rows:4:ticketAmount": {
            "type": "string",   # College student ticket (Taiwan only)
            "enum": ["0P", "1P", "2P", "3P", "4P", "5P", "6P", "7P", "8P", "9P", "10P"]
        },
        "homeCaptcha:securityCode": {"type": "string"}
    },
    "required": [
        "selectStartStation", "selectDestinationStation", "toTimeTable",
        "homeCaptcha:securityCode"
    ],
    "additionalProperties": False
}

CONFIRM_TRAIN_SCHEMA: Mapping[str, Any] = {
    "type": "object",
    "properties": {
        "BookingS2Form:hf:0": {"type": "string"},
        "TrainQueryDataViewPanel:TrainGroup": {"type": "string"}
    },
    "required": ["TrainQueryDataViewPanel:TrainGroup"],
    "additionalProperties": False
}

CONFIRM_TICKET_SHEMA: Mapping[str, Any] = {
    "type": "object",
    "properties": {
        "BookingS3FormSP:hf:0": {"type": "string"},
        "diffOver": {"type": "integer"},
        "idInputRadio": {"type": "string"},
        "idInputRadio:idNumber": {"type": "string"},
        "eaiPhoneCon:phoneInputRadio": {"type": "string"},
        "eaiPhoneCon:phoneInputRadio:mobilePhone": {"type": "string"},
        "email": {"type": "string"},
        "agree": {"type": "string", "enum": ["on", ""]},
        "isGoBackM": {"type": "string"},
        "backHome": {"type": "string"},
        "TgoError": {"type": "string"}
    },
    "required": ["agree", "idInputRadio:idNumber"],
    "additionalProperties": False
}
