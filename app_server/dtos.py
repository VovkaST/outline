from contextlib import suppress

from pydantic import BaseModel, Field, model_validator

# class GetURLRequest(BaseModel):
#     task_id: str = Field(title="Идентификатор задания на оплату")
#     customer_key: str = Field(title="Идентификатор покупателя")


class PaymentResponse(BaseModel):
    TerminalKey: str | None = Field(title="Идентификатор терминала", default=None)
    Amount: int | None = Field(title="Сумма в копейках", default=None)
    OrderId: str | None = Field(title="Идентификатор заказа в системе мерчанта", default=None)
    Success: bool | None = Field(title="Успешность прохождения запроса")
    Status: str | None = Field(title="Статус транзакции", default=None)
    PaymentId: str | None = Field(title="Идентификатор платежа в системе Т‑Кассы", default=None)
    ErrorCode: str | None = Field(title="Код ошибки. 0 в случае успеха", default="0")
    Message: str | None = Field(title="Краткое описание ошибки", default=None)
    Details: str | None = Field(title="Подробное описание ошибки", default=None)

    def dump_error(self) -> dict[str, str]:
        return self.model_dump(include={"ErrorCode", "Message", "Details"})


class InitPaymentResponse(PaymentResponse):
    PaymentURL: str | None = Field(title="Ссылка на платежную форму", default=None)


class SubscriptionRejectRequest(BaseModel):
    task_guid: str


class NotificationPaymentRequest(BaseModel):
    TerminalKey: str | None = Field(title="Идентификатор терминала", default=None)
    Amount: int | None = Field(title="Сумма в копейках", default=None)
    OrderId: str | None = Field(title="Идентификатор заказа в системе мерчанта", default=None)
    Success: bool | None = Field(title="Успешность прохождения запроса", default=None)
    Status: str | None = Field(title="Статус платежа", default=None)
    PaymentId: int | None = Field(title="Уникальный идентификатор транзакции в системе Т‑Кассы", default=None)
    ErrorCode: str | None = Field(title="Код ошибки. 0 в случае успеха", default=None)
    Message: str | None = Field(title="Краткое описание ошибки", default=None)
    Details: str | None = Field(title="Подробное описание ошибки", default=None)
    RebillId: int | None = Field(title="Идентификатор автоплатежа", default=None)
    CardId: int | None = Field(title="Идентификатор карты в системе Т‑Кассы", default=None)
    Pan: str | None = Field(title="Замаскированный номер карты или телефона", default=None)
    ExpDate: str | None = Field(
        title="Срок действия карты в формате MMYY, где YY — две последние цифры года", default=None
    )
    Token: str | None = Field(
        title="Подпись запроса. Формируется по такому же принципу, как и в случае запросов в Т‑Кассу.", default=None
    )
    Data: dict | None = Field(
        title="Дополнительные параметры платежа, переданные при создании заказа. ", default_factory=dict
    )

    @model_validator(mode="before")
    @classmethod
    def _pre_validator(cls, data):
        for data_key in ["data", "DATA"]:
            with suppress(KeyError):
                data["Data"] = data.pop(data_key)
        return data


class PaymentChargeRequest(BaseModel):
    task_guid: str = Field(title="Идентификатор задания на оплату")
