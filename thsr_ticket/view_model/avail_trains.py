from typing import List
from bs4.element import Tag

from thsr_ticket.view_model.abstract_view_model import AbstractViewModel
from thsr_ticket.configs.web.parse_avail_train import ParseAvailTrain
from thsr_ticket.configs.web.param_schema import Train



class AvailTrains(AbstractViewModel):
    def __init__(self) -> None:
        super(AvailTrains, self).__init__()
        self.avail_trains: List[Train] = []
        self.cond = ParseAvailTrain()

    def parse(self, html: bytes) -> List[Train]:
        page = self._parser(html)
        avail = page.find_all('label', **self.cond.from_html)
        return self._parse_train(avail)

    def _parse_train(self, avail: List[Tag]) -> List[Train]:
        for item in avail:
            train_id = int(item.find(**self.cond.train_id).text)
            depart_time = item.find(**self.cond.depart).text
            arrival_time = item.find(**self.cond.arrival).text
            travel_time = item.find(**self.cond.duration).find_next(
                'span', {'class': 'material-icons'}
            ).fetchNextSiblings()[0].text
            discount_str = self._parse_discount(item)
            form_value = item.find(**self.cond.form_value).attrs['value']
            self.avail_trains.append(
                Train(
                    id=train_id,
                    depart=depart_time,
                    arrive=arrival_time,
                    travel_time=travel_time,
                    discount_str=discount_str,
                    form_value=form_value,
                )
            )
        return self.avail_trains

    def _parse_discount(self, item: Tag) -> str:
        discounts = []
        if tag := item.find(**self.cond.early_bird_discount):
            discounts.append(tag.find_next().text)
        if tag := item.find(**self.cond.college_student_discount):
            discounts.append(tag.find_next().text)
        if discounts:
            joined_str = ', '.join(discounts)
            return f'({joined_str})'
        return ''
