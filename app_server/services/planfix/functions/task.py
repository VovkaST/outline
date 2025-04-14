class Task:
    TEMPLATE_FOLDER = "task/"

    def __init__(self, base):
        self.api = base

    async def get(self, **kwargs):
        """
        https://planfix.com/ru/help/ПланФикс_API_task.get
        """
        return await self.api.make_request(self.TEMPLATE_FOLDER + "get.xml", method="post", **kwargs)
