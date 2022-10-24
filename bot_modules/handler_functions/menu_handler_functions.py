from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot_modules import utils

send_message = utils.send_message
edit_message = utils.edit_message

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not "has_used_bot" in context.user_data.keys():
        context.user_data["has_used_bot"] = True
        text = "👋 Welcome to the bot. To get started, use one of the buttons below to navigate the bot. Since this is probably your first time using the bot, you should probably create a client first using the respective button.\n\n🟢 <b>Main menu</b>\n\nUse the options below the main menu 👇 to get started!"
    else:
        text = "🟢 <b>Main menu</b>\n\nUse the options below the main menu 👇 to get started!"

    keyboard = utils.Keyboards.main_menu
    if update.callback_query:
        await update.callback_query.answer()
        await edit_message(update, text, keyboard)
    else:
        await send_message(context, update, text, keyboard)

    return ConversationHandler.END
