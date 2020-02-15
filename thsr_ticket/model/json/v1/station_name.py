from thsr_ticket.model.json.base_response import BaseResponse


class StationName(BaseResponse):
    def __init__(self) -> None:
        super(StationName, self).__init__()
        self.Zh_tw: str = None
        self.En: str = None
