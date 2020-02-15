from thsr_ticket.model.json.base_response import BaseResponse
from thsr_ticket.model.json.v1.station_name import StationName


class DailyTrainInfo(BaseResponse):
    def __init__(self) -> None:
        super(DailyTrainInfo, self).__init__()
        self.TrainNo: int = None
        self.Direction: int = None
        self.StartingStationID: int = None
        self.StartingStationName: object = StationName()
        self.EndingStationID: int = None
        self.EndingStationName: object = StationName()
        self.Note: dict = None
