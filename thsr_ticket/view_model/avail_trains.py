from typing import List, Mapping
from collections import namedtuple
from bs4.element import Tag

from thsr_ticket.view_model.abstract_view_model import AbstractViewModel
from thsr_ticket.configs.web.parse_avail_train import ParseAvailTrain

Train = namedtuple("Train", ["id", "depart", "arrive", "travel_time", "discount", "form_value"])


class AvailTrains(AbstractViewModel):
    def __init__(self) -> None:
        super(AvailTrains, self).__init__()
        self.avail_trains: List[Train] = []
        self.cond = ParseAvailTrain()

    def parse(self, html: bytes) -> List[Train]:
        page = self._parser(html)
        avail = page.find_all("tr", **self.cond.from_html)
        return self._parse_train(avail)

    def _parse_train(self, avail: List[Tag]) -> List[Train]:
        for item in avail:
            train_id = item.find(**self.cond.train_id).text
            depart_time = item.find(**self.cond.depart).text
            arrival_time = item.find(**self.cond.arrival).text
            travel_time = item.find(**self.cond.arrival).parent.fetchNextSiblings()[0].text
            discount = self._parse_discount(item)
            form_value = item.find(**self.cond.form_value).attrs["value"]
            self.avail_trains.append(Train(
                train_id, depart_time, arrival_time, travel_time, discount, form_value
            ))
        return self.avail_trains

    def _parse_discount(self, item: Tag) -> Mapping[str, str]:
        img_list = item.find_all("img")
        discounts = {}
        for img in img_list:
            link = img.attrs["src"]
            gif = link.split("/")[-1]
            name = gif.split(".")[0]
            if name.startswith("irs_ind"):
                # Early discount
                discounts["Early"] = self.cond.discount_keyword[name]
            elif name.endswith("off"):
                # College student discount
                discounts["College"] = self.cond.discount_keyword[name]
        return discounts
