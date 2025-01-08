from typing import Iterable

from thsr_ticket.model.db import Record
from thsr_ticket.model.web.booking_form.station_mapping import StationMapping


def history_info(hists: Iterable[Record], select: bool = True) -> int:
    for idx, r in enumerate(hists, 1):
        print("第{}筆紀錄".format(idx))
        print("  身分證字號: " + r.personal_id)
        print("  手機號碼: " + r.phone)
        print("  起程站: " + StationMapping(r.start_station).name)
        print("  到達站: " + StationMapping(r.dest_station).name)
        t_str = r.outbound_time
        print("  出發時間: {}:{} (A: 早上, P: 下午, N: 中午)".format(t_str[:-3], t_str[-3:]))
        print("  大人票數: " + r.adult_num[:-1])
        print("  出發日期: " + r.outbound_date)
        print("  最晚可接受時間: " + r.outbound_delay_time + "點\n")

    if select:
        use_history = input('是否使用歷史紀錄？(y/n，預設n)：').lower() or 'n'
        if use_history == 'y':
            sel = input("請選擇紀錄（預設：1）：") or "1"
            return int(sel) - 1
    return None
