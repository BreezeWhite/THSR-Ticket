from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from thsr_ticket.model.db import Record

def _format_station_name(station_id: int) -> str:
    """將車站編號轉換為站名"""
    stations = {
        1: "南港", 2: "台北", 3: "板橋", 4: "桃園", 5: "新竹",
        6: "苗栗", 7: "台中", 8: "彰化", 9: "雲林", 10: "嘉義",
        11: "台南", 12: "左營"
    }
    return stations.get(station_id, str(station_id))

def history_info(hist: List['Record']) -> int:
    """顯示歷史紀錄並讓用戶選擇

    Args:
        hist (List[Record]): 歷史紀錄列表

    Returns:
        int: 用戶選擇的索引，如果沒有選擇則返回 None
    """
    print(f"歷史紀錄數量: {len(hist) if hist else 0}")
    if not hist:
        return None

    print('\n是否使用歷史紀錄：')
    print('-' * 50)
    for idx, h in enumerate(hist):
        print(f"{idx + 1}. 身分證字號: {h.personal_id}")
        print(f"   電話號碼: {h.phone}")
        print(f"   行程: {_format_station_name(h.start_station)} → {_format_station_name(h.dest_station)}")
        print(f"   日期: {h.outbound_date}")
        print(f"   時間: {h.outbound_time}")
        print(f"   票數: {h.adult_num[0]} 張全票")
        print('-' * 50)
    
    try:
        choice = input("\n請選擇要使用的歷史紀錄（輸入數字），直接按 Enter 則不使用歷史紀錄：")
        if not choice:
            return None
        idx = int(choice) - 1
        if 0 <= idx < len(hist):
            return idx
    except ValueError:
        pass
    return None 