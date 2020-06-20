import sys
sys.path.append("./")

from thsr_ticket.remote.endpoint_client import EndpointClient
from thsr_ticket.model.json.v1.train import Train
from thsr_ticket.controller.booking_flow import BookingFlow


if __name__ == "__main__":
    #client = EndpointClient()
    #resp = client.get_trains_by_date("2020-01-25")
    #train = Train().from_json(resp[0])

    flow = BookingFlow()
    result = flow.run()
