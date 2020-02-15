from typing import List
from collections import namedtuple

from thsr_ticket.view_model.abstract_view_model import AbstractViewModel
from thsr_ticket.configs.web.parse_html_element import ERROR_FEEDBACK

Error = namedtuple("Error", ["msg"])


class ErrorFeedback(AbstractViewModel):
    def __init__(self) -> None:
        super(ErrorFeedback, self).__init__()
        self.errors: List[Error] = []

    def parse(self, html: bytes) -> List[Error]:
        page = self._parser(html)
        items = page.find_all(**ERROR_FEEDBACK)
        for it in items:
            self.errors.append(Error(it.text))

        return self.errors
