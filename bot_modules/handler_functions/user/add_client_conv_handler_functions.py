from telegram import (
    Update,
)
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)

from bot_modules import utils

send_message = utils.send_message
edit_message = utils.edit_message
signal_regex = utils.signal_regex


# /////////////////////////////////////////////////////////////////////////////////
# New client conversation
# /////////////////////////////////////////////////////////////////////////////////
async def start_new_client_conv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    if not "clients" in context.user_data.keys():
        context.user_data["clients"] = {}
    context.user_data[
        "default_name"
    ] = f"Client{len(context.user_data['clients'].keys()) + 1}"
    text = f"❗ Enter a custom name for the client, or accept the recommended default name of <b>{context.user_data['default_name']}</b>"

    keyboard = utils.Keyboards.new_client_name
    await edit_message(update, text, keyboard)

    return "add_client_conv.states.client_name"


async def get_custom_client_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()
    new_client_name = update.message.text

    if new_client_name == "":
        text = f"❕ Client name was left empty. Please enter a valid name."
        keyboard = utils.Keyboards.end_new_client_conv
        await send_message(context, update, text, keyboard)

        return "add_client_conv.states.client_name"
    # If the client name already exists
    elif new_client_name in context.user_data["clients"].keys():
        text = f"❕ Client with name {new_client_name} already exists. Please enter a different name."
        keyboard = utils.Keyboards.end_new_client_conv
        await send_message(context, update, text, keyboard)

        return "add_client_conv.states.client_name"
    else:
        context.user_data["new_client_name"] = update.message.text.strip()

        text = f"✅ Client name set to {context.user_data['new_client_name']}.\n\n❗ Now enter your API key."
        keyboard = utils.Keyboards.back_to_main
        await send_message(context, update, text, keyboard)

        return "add_client_conv.states.client_api_key"


async def accept_default_client_name(
        update: Update, context: ContextTypes.DEFAULT_TYPE
):
    context.user_data["new_client_name"] = context.user_data["default_name"]

    text = f"✅ Client name set to {context.user_data['new_client_name']}.\n\n❗ Now enter your API key."
    keyboard = utils.Keyboards.end_new_client_conv
    if update.callback_query:
        await update.callback_query.answer()
        await edit_message(update, text, keyboard)
    else:
        await send_message(context, update, text, keyboard)

    return "add_client_conv.states.client_api_key"


async def get_client_api_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    context.user_data["new_api_key"] = update.message.text.strip()

    text = f"💡 Entered API key {context.user_data['new_api_key']}. \n\n❗ Now enter your secret key:"
    keyboard = utils.Keyboards.end_new_client_conv
    await send_message(context, update, text, keyboard)

    return "add_client_conv.states.client_secret_key"


async def get_client_secret_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    context.user_data["new_secret_key"] = update.message.text.strip()

    text = f"💡 <b>Your entered info:</b>\n\n<b>Client name:</b> {context.user_data['new_client_name']}\n\n<b>API key:</b> {context.user_data['new_api_key']}\n\n<b>Secret key:</b> {context.user_data['new_secret_key']}\n\nType /confirm to finish creating the client."
    keyboard = utils.Keyboards.end_new_client_conv
    await send_message(context, update, text, keyboard)

    return "add_client_conv.states.confirm"


async def confirm_client_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    context.user_data["clients"][context.user_data["new_client_name"]] = {}
    context.user_data["clients"][context.user_data["new_client_name"]][
        "api_key"
    ] = context.user_data["new_api_key"]
    context.user_data["clients"][context.user_data["new_client_name"]][
        "secret_key"
    ] = context.user_data["new_secret_key"]

    text = (
        f"✅ Client <b>{context.user_data['new_client_name']}</b> successfully created."
    )
    keyboard = utils.Keyboards.back_to_main
    await send_message(context, update, text, keyboard)

    del context.user_data["new_api_key"]
    del context.user_data["new_secret_key"]
    del context.user_data["new_client_name"]

    return ConversationHandler.END


async def end_new_client_conv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    text = "❌ New client operation canceled."
    keyboard = utils.Keyboards.back_to_main
    await edit_message(update, text, keyboard)

    return ConversationHandler.END
