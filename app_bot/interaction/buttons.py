from contrib.enums import TextChoices


class BotButtons(TextChoices):
    MAIN_MENU = "MAIN_MENU", "🏠 Главное меню"
    BACKWARD = "BACKWARD", "⬅️ Назад"

    CONNECT = "CONNECT", "📥 Подключиться"
    GET_TOKEN = "GET_TOKEN", "🎁 Получить ключ"
    PAY = "PAY", "💰 Оплатить/Продлить"
    PAY_1MON = "PAY_1MON", "🕐 1 мес — 199 ₽"
    PAY_3MON = "PAY_3MON", "🕑 3 мес — 499 ₽"
    PAY_6MON = "PAY_6MON", "🗓 6 мес + 1️⃣ в подарок 🎁 — 999 ₽"
    PAY_12MON = "PAY_12MON", "📅 12 мес + 3️⃣ в подарок 🎁 — 1999 ₽"
    INSTALL = "INSTALL", "📄 Установить VPN"
    REFERAL = "REFERAL", "👥 Создать партнерскую ссылку"
    HELP = "HELP", "🛠 Помощь"

    IOS = "IOS", "🍏 iOS/Айфон"
    ANDROID = "ANDROID", "🤖 Android"
    DOWNLOAD_APP = "DOWNLOAD_APP", "⬇️ Скачать приложение"
    IOS_DOWNLOAD = "IOS_DOWNLOAD", "⬇️ iOS"
    ANDROID_DOWNLOAD = "ANDROID_DOWNLOAD", "⬇️ Android"
