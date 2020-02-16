from typing import List

from thsr_ticket.view.web.abstract_show import AbstractShow
from thsr_ticket.view_model.error_feedback import Error


class ShowErrorMsg(AbstractShow):
    def show(self, errors: List[Error], select: bool = False) -> int:
        for e in errors:
            print("錯誤: {}".format(e.msg))
        return 0
