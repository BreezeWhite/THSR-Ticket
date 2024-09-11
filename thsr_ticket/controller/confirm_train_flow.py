import json
from typing import List, Tuple

from requests.models import Response

from thsr_ticket.model.db import Record
from thsr_ticket.remote.http_request import HTTPRequest
from thsr_ticket.view_model.avail_trains import AvailTrains
from thsr_ticket.configs.web.param_schema import Train, ConfirmTrainModel



class ConfirmTrainFlow:
    def __init__(self, client: HTTPRequest, book_resp: Response, record: Record = None):
        self.client = client
        self.book_resp = book_resp
        self.record = record

    def run(self) -> Tuple[Response, ConfirmTrainModel]:
        trains = AvailTrains().parse(self.book_resp.content)
        if not trains:
            raise ValueError('No available trains!')
        elif trains[0].depart.startswith(self.record.outbound_delay_time):
            raise ValueError('too late to go home')

        confirm_model = ConfirmTrainModel(
            selected_train=self.select_available_trains(trains),
        )
        json_params = confirm_model.json(by_alias=True)
        dict_params = json.loads(json_params)
        resp = self.client.submit_train(dict_params)
        return resp, confirm_model

    def select_available_trains(self, trains: List[Train], default_value: int = 1) -> Train:
        # for idx, train in enumerate(trains, 1):
        #     print(
        #         f'{idx}. {train.id:>4} {train.depart:>3}~{train.arrive} {train.travel_time:>3} '
        #         f'{train.discount_str}'
        #     )
        # selection = int(input(f'輸入選擇（預設：{default_value}）：') or default_value)
        # return trains[selection-1].form_value
        return trains[0].form_value
