import os
from typing import Mapping, List, Iterable, Any, NamedTuple

from tinydb import TinyDB, Query
from tinydb.database import Document

from thsr_ticket import MODULE_PATH
from thsr_ticket.configs.web.param_schema import ConfirmTicketModel


class Record(NamedTuple):
    personal_id: str = None
    phone: str = None
    start_station: int = None
    dest_station: int = None
    outbound_time: str = None
    adult_num: str = None
    outbound_date: str = None
    outbound_delay_time: str = None


class ParamDB:
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = os.path.join(MODULE_PATH, ".db", "history.json")
        self.db_path = db_path
        db_dir = db_path[:db_path.rfind("/")]
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

    def save(self, record: Record, ticket: ConfirmTicketModel) -> None:
        data = Record(
            ticket.personal_id,
            ticket.phone_num,
            record.start_station,
            record.dest_station,
            record.outbound_time,
            record.adult_num,
            record.outbound_date,
            record.outbound_delay_time
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
