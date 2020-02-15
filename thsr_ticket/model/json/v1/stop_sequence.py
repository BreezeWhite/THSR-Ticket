from thsr_ticket.model.json.base_response import BaseResponse
from thsr_ticket.model.json.v1.station_name import StationName


class StopSequence(BaseResponse):
    def __init__(self) -> None:
        super(StopSequence, self).__init__()
        self.StopSequence: int = None
        self.StationID: int = None
        self.StationName: object = StationName()
        self.ArrivalTime: str = None
        self.DepartureTime: str = None
