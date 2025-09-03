from contrib.enums import TextChoices


class BotButtons(TextChoices):
    MAIN_MENU = "MAIN_MENU", "🏠 Главное меню"
    BACKWARD = "BACKWARD", "⬅️ Назад"

    CONNECT = "CONNECT", "📥 Подключиться"
    GET_TOKEN = "GET_TOKEN", "🎁 Получить ключ"
    PAY = "PAY", "💰 Выбери свой тариф"
    PAY_1MON = "PAY_1MON", "1️⃣ месяц"
    PAY_3MON = "PAY_3MON", "3️⃣ месяца"
    PAY_6MON = "PAY_6MON", "6️⃣ месяцев + 1️⃣ в подарок 🎁"
    PAY_12MON = "PAY_12MON", "1️⃣2️⃣ месяцев + 3️⃣ в подарок 🎁"
    INSTALL = "INSTALL", "📄 Установить VPN"
    REFERAL = "REFERAL", "👥 Создать партнерскую ссылку"
    HELP = "HELP", "🛠 Помощь"

    IOS = "IOS", "🍏 iOS"
    ANDROID = "ANDROID", "🤖 Android"
    IOS_DOWNLOAD = "IOS_DOWNLOAD", "⬇️ iOS"
    ANDROID_DOWNLOAD = "ANDROID_DOWNLOAD", "⬇️ Android"
