from contrib.enums import TextChoices


class BotCommands(TextChoices):
    START = "start", "Запустить бота"
    # HELP = "help", "Помощь"


class UpdateMode(TextChoices):
    POLLING = "polling", "Long polling"
    WEBHOOK = "webhook", "Webhook"
