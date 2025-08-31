from contrib.enums import TextChoices


class BotCommands(TextChoices):
    START = "start", "Запустить бота"
    HELP = "help", "Помощь"
