import hmac
import base64
from datetime import datetime

import requests

from thsr_ticket.configs.rest.endpoints import Endpoints as ep

# Key for hmac
KEY = "FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF"


class EndpointClient:
    def __init__(self) -> None:
        self.client = requests.session()

    def get_trains_by_date(self, date: str) -> dict:
        # date: yyyy-mm-dd
        return self.client.get(ep.TRAINS_BY_DATE.format(date), headers=get_header()).json()

    def get_trains_by_ori_dest_station(self, origin_id: int, dest_id: int, date: str) -> dict:
        return self.client.get(
            ep.TRAINS_BY_ORI_DEST_STATION.format(origin_id, dest_id, date),
            headers=get_header()
        ).json()


def auth_x_date(date: str) -> str:
    key = bytearray()
    key.extend(map(ord, KEY))
    mac = hmac.new(key, msg=date.encode("ascii"), digestmod='sha1')
    return base64.b64encode(mac.digest()).decode("utf-8")


def get_x_date() -> str:
    now = datetime.utcnow()
    today = now.ctime()
    date, mon, day, time, year = str(today).split(" ")
    return "{}, {} {} {} {} GMT".format(date, day, mon, year, time)


def get_header() -> dict:
    x_date = get_x_date()
    auth = auth_x_date("x-date: "+x_date)
    auth_str = """
        hmac username="FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF",
        algorithm='hmac-sha1',
        headers='x-date',
        signature='{}'
    """.format(auth)

    head = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-TW,zh;q=0.8,en-US;q=0.5,en;1=0.3",
        "Authorization": auth_str,
        "Connection": "keep-alive",
        "DNT": "1",
        "Host": "ptx.transportdata.tw",
        "Referer": "https://ptx.transportdata.tw/MOTC?t=Rail&v=2",
        "x-date": x_date
    }

    return head
