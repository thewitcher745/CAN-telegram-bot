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

Client = utils.Client


# /////////////////////////////////////////////////////////////////////////////////
# New client conversation
# /////////////////////////////////////////////////////////////////////////////////
async def start_add_client_conv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()
    context.user_data["user"].new_client = Client()

    text = f"❕ Enter a custom name for the client, or accept the recommended default name of <b>{context.user_data['user'].get_next_default_name()}</b>"
    keyboard = utils.Keyboards.AddClient.name
    await edit_message(update, text, keyboard)

    return "add_client_conv.states.client_name"


async def get_custom_client_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    new_client_name = update.message.text.strip()

    # If the client name is empty
    if new_client_name == "":
        text = f"❕ Client name was left empty. Please enter a valid name."
        keyboard = utils.Keyboards.AddClient.end_conv
        await send_message(context, update, text, keyboard)

        return "add_client_conv.states.client_name"

    # If the client name already exists
    elif context.user_data["user"].client_name_exists(new_client_name):
        text = f"❕ Client with name {new_client_name} already exists. Please enter a different name."
        keyboard = utils.Keyboards.AddClient.end_conv
        await send_message(context, update, text, keyboard)

        return "add_client_conv.states.client_name"
    else:
        context.user_data["user"].new_client.name = update.message.text.strip()

        text = f"✅ Client name set to {context.user_data['user'].new_client.name}.\n\n❗ Select the name of the exchange associated with this client."
        keyboard = utils.Keyboards.AddClient.exchange
        await send_message(context, update, text, keyboard)

        return "add_client_conv.states.exchange"


async def accept_default_client_name(
        update: Update, context: ContextTypes.DEFAULT_TYPE
):
    context.user_data["user"].new_client.name = context.user_data["user"].get_next_default_name()

    text = f"✅ Client name set to {context.user_data['user'].new_client.name}.\n\n❗ Select the name of the exchange associated with this client."
    keyboard = utils.Keyboards.AddClient.exchange
    if update.callback_query:
        await update.callback_query.answer()
        await edit_message(update, text, keyboard)
    else:
        await send_message(context, update, text, keyboard)

    return "add_client_conv.states.exchange"


async def select_exchange(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    context.user_data["user"].new_client.exchange_id = update.callback_query.data[len("add_client_exchange:"):]

    text = f"💡 You selected {context.user_data['user'].new_client.exchange_id} as this client's exchange. \n\n❗ Now select the account type:"
    keyboard = utils.Keyboards.AddClient.account_type
    await edit_message(update, text, keyboard)

    return "add_client_conv.states.account_type"


async def select_account_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    context.user_data["user"].new_client.account_type = update.callback_query.data[len("add_client_account_type:"):]

    text = f"💡 You selected {context.user_data['user'].new_client.account_type} as this client's account type. \n\n❗ Now you need to enter the API key, which will be used to authenticate with the exchange:"
    keyboard = utils.Keyboards.AddClient.end_conv
    await edit_message(update, text, keyboard)

    return "add_client_conv.states.client_api_key"


async def get_client_api_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    context.user_data["user"].new_client.api_key = update.message.text.strip()

    text = f"💡 Entered API key {context.user_data['user'].new_client.api_key}. \n\n❗ Now enter your exchange account's secret key:"
    keyboard = utils.Keyboards.AddClient.end_conv
    await send_message(context, update, text, keyboard)

    return "add_client_conv.states.client_secret_key"


async def get_client_secret_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    context.user_data["user"].new_client.secret_key = update.message.text.strip()

    text = f"💡 <b>Your entered info:</b>\n\n<b>Client name:</b> {context.user_data['user'].new_client.name}\n\n" \
           f"<b>Exchange:</b> {context.user_data['user'].new_client.exchange_id}\n\n" \
           f"<b>Account type:</b> {context.user_data['user'].new_client.account_type}\n\n" \
           f"<b>API key:</b> {context.user_data['user'].new_client.api_key}\n\n" \
           f"<b>Secret key:</b> {context.user_data['user'].new_client.secret_key}\n\n" \
           f"Type /confirm to finish creating the client."

    keyboard = utils.Keyboards.AddClient.end_conv
    await send_message(context, update, text, keyboard)

    return "add_client_conv.states.confirm"


async def confirm_client_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    context.user_data["user"].add_client(context.user_data["user"].new_client)
    context.user_data["user"].new_client = None

    text = (
        f"✅ Client <b>{context.user_data['user'].clients[-1].name}</b> successfully created."
    )
    keyboard = utils.Keyboards.back_to_main
    await send_message(context, update, text, keyboard)

    return ConversationHandler.END


async def end_new_client_conv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    text = "❌ New client operation canceled."
    keyboard = utils.Keyboards.back_to_main
    await edit_message(update, text, keyboard)

    return ConversationHandler.END
