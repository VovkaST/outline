from contrib.enums import TextChoices


class BotButtons(TextChoices):
    BACKWARD = "BACKWARD", "⬅️ Назад"

    CONNECT = "CONNECT", "📥 Подключиться"

    IOS = "IOS", "🍏 iOS"
    ANDROID = "ANDROID", "🤖 Android"
    IOS_DOWNLOAD = "IOS_DOWNLOAD", "⬇️ iOS"
    ANDROID_DOWNLOAD = "ANDROID_DOWNLOAD", "⬇️ Android"
