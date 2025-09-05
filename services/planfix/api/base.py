from services.http_service import BaseHTTPService


class BaseAPIEntity:
    def __init__(self, base):
        self.api: BaseHTTPService = base
