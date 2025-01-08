import sys
import time
import random
sys.path.append("./")

from thsr_ticket.remote.endpoint_client import EndpointClient
from thsr_ticket.model.json.v1.train import Train
from thsr_ticket.controller.booking_flow import BookingFlow


def main():
    flow = BookingFlow()
    status = flow.run()
    return status


if __name__ == "__main__":
    status = ''
    while 1:
        if status == 'finish':
            break
        status = main()
        time.sleep(random.randint(5, 10))
