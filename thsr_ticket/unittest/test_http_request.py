from thsr_ticket.remote.http_request import HTTPRequest


def test_requests_work():
    client = HTTPRequest()

    resp = client.request_booking_page()
    assert resp.status_code == 200
    assert client.request_security_code_img(resp.content).status_code == 200
