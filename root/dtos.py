from pydantic import BaseModel, ConfigDict, Field


class ErrorResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    ErrorCode: str | None = Field(title="Код ошибки. 0 в случае успеха", default="0", alias="error_code")
    Message: str | None = Field(title="Краткое описание ошибки", default=None, alias="message")
    Details: str | None = Field(title="Подробное описание ошибки", default=None, alias="details")

    def dump_error(self) -> dict[str, str]:
        return self.model_dump(include={"ErrorCode", "Message", "Details"}, by_alias=True)


class RequestStatusResponse(BaseModel):
    success: bool = Field(title="Успешность запроса")
    message: str | None = Field(title="Сообщение о результате запроса", default=None)


class OkResponse(BaseModel):
    success: bool = Field(title="Успешность запроса", default=True)
    message: str | None = Field(title="Сообщение о результате запроса", default="OK")
