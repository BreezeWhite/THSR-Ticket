
class HTTPConfig:
    BOOKING_PAGE_URL = "https://irs.thsrc.com.tw/IMINT/?locale=tw"
    SECURE_CODE_URL = "https://irs.thsrc.com.tw/IMINT/?wicket:interface=:0:BookingS1Form:homeCaptcha:passCode::IResourceListener&wicket:antiCache=1579440790196"
    SUBMIT_FORM_URL = "https://irs.thsrc.com.tw/IMINT/;jsessionid={}?wicket:interface=:0:BookingS1Form::IFormSubmitListener"
    CONFIRM_TRAIN_URL = "https://irs.thsrc.com.tw/IMINT/?wicket:interface=:1:BookingS2Form::IFormSubmitListener"
    CONFIRM_TICKET_URL = "https://irs.thsrc.com.tw/IMINT/?wicket:interface=:2:BookingS3Form::IFormSubmitListener"

    class HTTPHeader:
        USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0"
        ACCEPT_HTML = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        ACCEPT_IMG = "image/webp,*/*"
        ACCEPT_LANGUAGE = "zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3"
        ACCEPT_ENCODING = "gzip, deflate, br"

        # Host URL
        BOOKING_PAGE_HOST = "irs.thsrc.com.tw"
