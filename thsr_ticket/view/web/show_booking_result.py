from typing import List

from thsr_ticket.view.web.abstract_show import AbstractShow
from thsr_ticket.view_model.booking_result import Ticket


class ShowBookingResult(AbstractShow):
    def show(self, tickets: List[Ticket], select: bool = False) -> int:
        ticket = tickets[0]
        print("\n\n----------- 訂位結果 -----------")
        print("訂位代號: "+ticket.id)
        print("繳費期限: "+ticket.payment_deadline)
        print("總價: "+ticket.price)
        print("-"*20)
        hint = ["日期", "起程站", "到達站", "出發時間", "到達時間", "車次"]
        fmt = "{:>6}" * len(hint)
        print(fmt.format(*hint))
        info = [
            ticket.date, ticket.start_station, ticket.dest_station, ticket.depart_time,
            ticket.arrival_time, ticket.train_id
        ]
        print("    {}   {}     {}     {}    {}      {}".format(*info))
        print("    {} {}".format(ticket.seat_class, ticket.seat))
        return 0
