import os
from typing import Mapping, List, Iterable, Any, NamedTuple

from tinydb import TinyDB, Query
from tinydb.database import Document

from thsr_ticket.model.web.booking_form.booking_form import BookingForm
from thsr_ticket.model.web.confirm_ticket import ConfirmTicket


class Record(NamedTuple):
    personal_id: str = None
    phone: str = None
    start_station: int = None
    dest_station: int = None
    outbound_time: str = None
    adult_num: str = None


class ParamDB:
    def __init__(self, db_path: str = "./.db/history.json"):
        self.db_path = db_path
        db_dir = db_path[:db_path.rfind("/")]
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

    def save(self, book_form: BookingForm, ticket: ConfirmTicket) -> None:
        data = Record(
            ticket.personal_id,
            ticket.phone,
            book_form.start_station,
            book_form.dest_station,
            book_form.outbound_time,
            book_form.adult_ticket_num
        )._asdict()  # type: ignore
        with TinyDB(self.db_path, sort_keys=True, indent=4) as db:
            hist = db.search(Query().personal_id == ticket.personal_id)
            if self._compare_hist(data, hist) is None:
                db.insert(data)

    def get_history(self) -> List[Record]:
        with TinyDB(self.db_path) as db:
            dicts = db.all()
        return [Record(**d) for d in dicts]   # type: ignore

    def _compare_hist(self, data: Mapping[str, Any], hist: Iterable[Document]) -> int:
        for idx, h in enumerate(hist):
            comp = [h[k] for k in data.keys() if h[k] == data[k]]
            if len(comp) == len(data):
                return idx
        return None
