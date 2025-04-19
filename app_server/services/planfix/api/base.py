from app_server.services.base import BaseHTTPService


class BaseAPIEntity:
    def __init__(self, base):
        self.api: BaseHTTPService = base
