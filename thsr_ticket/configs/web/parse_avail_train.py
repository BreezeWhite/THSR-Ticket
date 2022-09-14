
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

    early_bird_discount = {
        'name': 'p',
        'attrs': {
            'class': 'early-bird'
        }
    }

    college_student_discount = {
        'name': 'p',
        'attrs': {
            'class': 'student'
        }
    }

    form_value = {
        "name": "input",
        "attrs": {
            "name": "TrainQueryDataViewPanel:TrainGroup"
        }
    }
