from typing import Mapping, Any
import requests
from requests.adapters import HTTPAdapter
from requests.models import Response


from thsr_ticket.configs.web.http_config import HTTPConfig


class HTTPRequest:
    def __init__(self, max_retries: int = 3) -> None:
        self.sess = requests.Session()
        self.sess.mount("https://", HTTPAdapter(max_retries=max_retries))

        self.common_head_html: dict = {
            "Host": HTTPConfig.HTTPHeader.BOOKING_PAGE_HOST,
            "User-Agent": HTTPConfig.HTTPHeader.USER_AGENT,
            "Accept": HTTPConfig.HTTPHeader.ACCEPT_HTML,
            "Accept-Language": HTTPConfig.HTTPHeader.ACCEPT_LANGUAGE,
            "Accept-Encoding": HTTPConfig.HTTPHeader.ACCEPT_ENCODING
        }

    def request_booking_page(self) -> Response:
        return self.sess.get(HTTPConfig.BOOKING_PAGE_URL, headers=self.common_head_html, allow_redirects=True)

    def request_security_code_img(self, book_page: bytes) -> Response:
        accept_img_head = self.common_head_html.copy()
        accept_img_head["Accept"] = "image/webp,*/*"
        param = {
            "wicket:interface": ":0:BookingS1Form:homeCaptcha:passCode::IResourceListener",
            "wicket:antiCache": self._parse_anti_cache(book_page.decode("UTF-8"))
        }
        return self.sess.get(HTTPConfig.SECURE_CODE_URL, headers=accept_img_head, params=param)

    def submit_booking_form(self, params: Mapping[str, Any]) -> Response:
        url = HTTPConfig.SUBMIT_FORM_URL.format(self.sess.cookies["JSESSIONID"])
        return self.sess.post(url, headers=self.common_head_html, params=params, allow_redirects=True)

    def _parse_anti_cache(self, html: str, keyword: str = "wicket:antiCache") -> str:
        start_idx = len(keyword)+html.find(keyword)+1
        end_idx = start_idx+html[start_idx:].find('">')
        return html[start_idx:end_idx]

    def submit_train(self, params: Mapping[str, Any]) -> Response:
        return self.sess.post(
            HTTPConfig.CONFIRM_TRAIN_URL,
            headers=self.common_head_html,
            params=params,
            allow_redirects=True
        )

    def submit_ticket(self, params: Mapping[str, Any]) -> Response:
        return self.sess.post(
            HTTPConfig.CONFIRM_TICKET_URL,
            headers=self.common_head_html,
            params=params,
            allow_redirects=True
        )
