from contrib.enums import TextChoices


class BotButtons(TextChoices):
    MAIN_MENU = "MAIN_MENU", "🏠 Главное меню"
    BACKWARD = "BACKWARD", "⬅️ Назад"

    CONNECT = "CONNECT", "📥 Подключиться"
    GET_TOKEN = "GET_TOKEN", "🎁 Получить ключ"
    PAY = "PAY", "💰 Оплатить"
    INSTALL = "INSTALL", "📄 Установить VPN"
    REFERAL = "REFERAL", "👥 Создать партнерскую ссылку"
    HELP = "HELP", "🛠 Помощь"

    IOS = "IOS", "🍏 iOS"
    ANDROID = "ANDROID", "🤖 Android"
    IOS_DOWNLOAD = "IOS_DOWNLOAD", "⬇️ iOS"
    ANDROID_DOWNLOAD = "ANDROID_DOWNLOAD", "⬇️ Android"
