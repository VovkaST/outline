from starlette.responses import JSONResponse


class SuccessResponse(JSONResponse):
    def render(self, content):
        message = {"success": True, "message": content}
        return super().render(message)
