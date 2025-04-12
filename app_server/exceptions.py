from app_server.dtos import PaymentResponse


class PaymentError(Exception):
    def __init__(self, response: PaymentResponse):
        self.response = response
