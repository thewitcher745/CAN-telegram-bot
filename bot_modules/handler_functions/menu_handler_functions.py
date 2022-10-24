from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot_modules import utils

send_message = utils.send_message
edit_message = utils.edit_message


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    text = (
        "🟢 Welcome to the bot.\nUse the options below the main menu 👇 to get started!"
    )

    await send_message(context, update, text)


async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "🟢 <b>Main menu</b>\n\nUse the buttons below to access different functions."
    keyboard = utils.Keyboards.main_menu

    if update.callback_query:
        await update.callback_query.answer()
        await edit_message(update, text, keyboard)
    else:
        await send_message(context, update, text, keyboard)

    return ConversationHandler.END
