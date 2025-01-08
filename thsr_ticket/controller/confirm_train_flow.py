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
        
        # 檢查第一班車是否太晚
        first_train_hour = int(trains[0].depart.split(':')[0])
        if first_train_hour >= int(self.record.outbound_delay_time):
            raise ValueError(f'太晚了！第一班車 {trains[0].depart} 已經超過限制時間 {self.record.outbound_delay_time}點')

        confirm_model = ConfirmTrainModel(
            selected_train=self.select_available_trains(trains),
        )
        json_params = confirm_model.json(by_alias=True)
        dict_params = json.loads(json_params)
        resp = self.client.submit_train(dict_params)
        return resp, confirm_model

    def select_available_trains(self, trains: List[Train], default_value: int = 1) -> Train:
        return trains[0].form_value
