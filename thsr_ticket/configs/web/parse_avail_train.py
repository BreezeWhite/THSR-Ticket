
class ParseAvailTrain:
    from_html = {
        "attrs": {
            "class": "result-item"
        }
    }

    train_id = {
        "id": "QueryCode"
    }

    depart = {
        "id": "QueryDeparture"
    }

    arrival = {
        "id": "QueryArrival"
    }

    duration = {
        "attrs": {
            "class": "duration"
        }
    }

    discount_keyword = {
        "irs_ind_ebH_zh_TW": "8折",
        "irs_ind_eb2_zh_TW": "9折",
        "irs_ind_ebX_zh_TW": "65折",
        "25off": "75折",
        "50off": "5折"
    }

    form_value = {
        "name": "input",
        "attrs": {
            "name": "TrainQueryDataViewPanel:TrainGroup"
        }
    }
