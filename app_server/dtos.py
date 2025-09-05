from contextlib import suppress

from pydantic import BaseModel, Field, model_validator

from root.config import settings
from root.dtos import ErrorResponse


class PaymentResponse(ErrorResponse):
    TerminalKey: str | None = Field(title="Идентификатор терминала", default=None)
    Amount: int | None = Field(title="Сумма в копейках", default=None)
    OrderId: str | None = Field(title="Идентификатор заказа в системе мерчанта", default=None)
    Success: bool | None = Field(title="Успешность прохождения запроса")
    Status: str | None = Field(title="Статус транзакции", default=None)
    PaymentId: str | None = Field(title="Идентификатор платежа в системе Т‑Кассы", default=None)


class PaymentQRResponse(PaymentResponse):
    Currency: int | None = Field(title="Код валюты по ISO 4217", default=None)


class InitPaymentResponse(PaymentResponse):
    PaymentURL: str | None = Field(title="Ссылка на платежную форму", default=None)


class PaymentStateResponse(PaymentResponse):
    Params: list[dict] | None = Field(
        title="Информация по способу оплаты или деталям для платежей в рассрочку", default_factory=list
    )


class GetQrResponse(ErrorResponse):
    PaymentURL: str | None = Field(title="Ссылка на платежную форму", default=None)
    TerminalKey: str | None = Field(title="Идентификатор терминала", default=None)
    OrderId: str | None = Field(title="Идентификатор заказа в системе мерчанта", default=None)
    Success: bool | None = Field(title="Успешность прохождения запроса")
    Data: str | None = Field(title="Информация, которая должна быть закодирована в QR", default=None)
    PaymentId: int | None = Field(title="Уникальный идентификатор транзакции в системе Т‑Кассы", default=None)
    RequestKey: str | None = Field(
        title="Идентификатор запроса на привязку счета. Передается в случае привязки и одновременной оплаты по CБП.",
        default=None,
    )


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


class NotificationQrRequest(BaseModel):
    TerminalKey: str = Field(title="Идентификатор терминала.", default=None)
    RequestKey: str = Field(title="Идентификатор запроса на привязку счета.", default=None)
    AccountToken: str = Field(title="Идентификатор привязки счета, назначаемый банком-эмитентом.", default=None)
    BankMemberId: str = Field(
        title="Идентификатор банка-эмитента клиента, который будет совершать оплату по привязанному счету — заполнен, "
        "если статус ACTIVE.",
        default=None,
    )
    BankMemberName: str = Field(
        title="Наименование банка-эмитента. Заполнен, если передан BankMemberId.",
        default=None,
    )
    NotificationType: str = Field(title="Тип уведомления, всегда — LINKACCOUNT.")
    Success: bool = Field(title="Успешность прохождения запроса", default=None)
    ErrorCode: str = Field(title="Код ошибки. 0 в случае успеха", default=None)
    Message: str = Field(title="Краткое описание ошибки", default=None)
    Token: str = Field(
        title="Подпись запроса. Формируется по такому же принципу, как и в случае запросов в Т‑Кассу.", default=None
    )
    Status: str = Field(title="Статус платежа", default=None)


class PaymentChargeRequest(BaseModel):
    task_guid: str = Field(title="Идентификатор задания на оплату")
    amount: int = Field(description="Сумма платежа в копейках (минимум 1000)", ge=1000)
    description: str = Field(description="Описание платежа", default=settings.DEFAULT_PAYMENT_DESCRIPTION)


class PutKeyRequest(BaseModel):
    guid: str = Field(description="Идентификатор ключа")
    key: str = Field(description="Ключ")
