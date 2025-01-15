import sys
import time
import random

sys.path.append("./")

from thsr_ticket.controller.booking_flow import BookingFlow
from thsr_ticket.model.db import ParamDB

def main():
    print("Press Ctrl+C to exit the program.")
    
    # 初始化數據庫和 flow
    db = ParamDB()
    flow = BookingFlow()
    
    # 獲取歷史紀錄
    record = db.get_history_record()
    if record:
        print(f"使用歷史紀錄：{record.personal_id}")
        flow.record = record
    
    while True:
        try:
            status = flow.run()
            if status == 'Finish':
                break
            # 保存當前的 record
            current_record = flow.record
            # 重新初始化 flow
            flow = BookingFlow()
            # 如果之前有 record，則保留
            if current_record:
                flow.record = current_record
            time.sleep(random.randint(1, 3))
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()
    