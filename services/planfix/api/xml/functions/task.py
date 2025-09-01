from services.planfix.api.base import BaseAPIEntity
from services.planfix.api.interfaces.task import ITask


class Task(BaseAPIEntity, ITask):
    TEMPLATE_FOLDER = "task/"

    async def get(self, **kwargs):
        """
        https://planfix.ru/docs/%D0%9F%D0%BB%D0%B0%D0%BD%D0%A4%D0%B8%D0%BA%D1%81_API_task.get
        """
        return await self.api.make_request(self.TEMPLATE_FOLDER + "get.xml", method="post", **kwargs)
