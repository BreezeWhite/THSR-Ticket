from typing import List

from thsr_ticket.view.web.abstract_show import AbstractShow
from thsr_ticket.view_model.avail_trains import Train


class ShowAvailTrains(AbstractShow):
    def __init__(self) -> None:
        pass

    def show(self, trains: List[Train], select: bool = True) -> int:
        if len(trains) == 0:
            print("No available train!")
            return None

        for idx, train in enumerate(trains, 1):
            dis_str = ""
            if "Early" in train.discount:
                dis_str += "早鳥{} ".format(train.discount["Early"])
            if "College" in train.discount:
                dis_str += "大學生{}".format(train.discount["College"])
            print("{}. {:>4s} {:>3}~{} {:>3} {:4}".format(
                idx, train.id, train.depart, train.arrive, train.travel_time, dis_str
            ))

        if select:
            return int(input("輸入選擇(預設: 1): ") or 1)
        return None
