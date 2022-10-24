from telegram import (
    InlineKeyboardButton,
    Update,
)
from telegram.ext import (
    ContextTypes,
)

from bot_modules import utils

send_message = utils.send_message
edit_message = utils.edit_message
signal_regex = utils.signal_regex


async def fetch_user_api_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    if utils.check_user_auth(context):
        keyboard = utils.Keyboards.back_to_main
        text = f'\n*️⃣ API key: {context.user_data["api_key"]}\n*️⃣ Secret key: {context.user_data["secret_key"]}'
        await edit_message(update, text, keyboard)

    else:
        text = '🟠 You haven\'t entered your API authentication information yet. \🤔\n\n✔ You can access your API info through your exchange, then use the "Enter/Change API key" option in the main menu or the menu below to provide the bot with your credentials. 💱'
        keyboard = utils.Keyboars.portfolio_no_clients
        await edit_message(update, text, keyboard)
