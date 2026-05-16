from contrib.enums import TextChoices


class BotButtons(TextChoices):
    MAIN_MENU = "MAIN_MENU", "🏠 Главное меню"
    BACKWARD = "BACKWARD", "⬅️ Назад"

    CONNECT = "CONNECT", "📥 Подключиться"
    GET_TOKEN = "GET_TOKEN", "🎁 Получить ключ"
    PAY = "PAY", "💰 Оплатить/Продлить"
    PAY_1MON = "PAY_1MON", "🕐 1 мес — 299 ₽"
    PAY_3MON = "PAY_3MON", "🕑 3 мес — 799 ₽"
    PAY_6MON = "PAY_6MON", "🗓 6 мес — 1499 ₽"
    PAY_12MON = "PAY_12MON", "📅 12 мес — 2999 ₽"
    INSTALL = "INSTALL", "📄 Установить VPN"
    REFERAL = "REFERAL", "👥 Создать партнерскую ссылку"
    HELP = "HELP", "🛠 Помощь"

    IOS_EU = "IOS_EU", "🍏 iOS/Айфон (🇪🇺 EU)"
    IOS_RU = "IOS_RU", "🍏 iOS/Айфон (🇷🇺 RU)"
    ANDROID = "ANDROID", "🤖 Android"
    DOWNLOAD_APP = "DOWNLOAD_APP", "⬇️ Скачать приложение"
    IOS_DOWNLOAD = "IOS_DOWNLOAD", "⬇️ iOS"
    ANDROID_DOWNLOAD = "ANDROID_DOWNLOAD", "⬇️ Android"
