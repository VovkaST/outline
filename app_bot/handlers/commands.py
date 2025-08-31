from telegram import Update
from telegram.ext import ContextTypes

from app_bot.interaction import menus
from app_bot.utils.context_history import clear_or_init_history


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    clear_or_init_history(context)
    user = update.effective_user
    text = menus.ConnectionMenu.format_message(first_name=user.first_name)
    bot = update.get_bot()
    await bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=menus.ConnectionMenu.keyboard)
    # await update.message.reply_text(text, reply_markup=menus.ConnectionMenu.keyboard)
