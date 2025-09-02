from telegram import Update
from telegram.ext import ContextTypes


async def user_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    text = update.message.text

    message_to_planfix = f"Сообщение от пользователя @{user.username or 'без username'} (ID: {user.id}):\n{text}"

    # Отправление в Planfix как комментарий к задаче
    send_to_planfix_chat(text, telegram_id=user_id, username=username)
