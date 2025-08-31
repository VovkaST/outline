from telegram import Update
from telegram.ext import ContextTypes

from app_bot.interaction import menus
from app_bot.interaction.messages import WELCOME


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    text = WELCOME.format(first_name=user.first_name)
    await update.message.reply_text(text, reply_markup=menus.connect_menu)
