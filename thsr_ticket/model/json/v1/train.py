from thsr_ticket.model.json.base_response import BaseResponse
from thsr_ticket.model.json.v1.daily_train_info import DailyTrainInfo
from thsr_ticket.model.json.v1.stop_sequence import StopSequence


class Train(BaseResponse):
    def __init__(self) -> None:
        super(Train, self).__init__()
        self.TrainDate: str = None
        self.DailyTrainInfo: object = DailyTrainInfo()
        self.StopTimes: list = [StopSequence()]
        self.UpdateTime: str = None
        self.VersionID: int = None
