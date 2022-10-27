from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot_modules import utils

send_message = utils.send_message
edit_message = utils.edit_message

Client = utils.Client


async def client_manager(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    client_name_list = [client.name for client in context.user_data["user"].clients]
    if len(client_name_list) > 0:
        text = "🟢 <b>Client manager menu</b>\n\nSelect the client you wish to edit:"
        keyboard = utils.Keyboards.ClientManager.client_list(client_name_list)
    else:
        text = "🟢 <b>Client manager menu</b>\n\nYou don't have any clients to edit. Add new clients first through main menu or the button below."
        keyboard = utils.Keyboards.ClientManager.empty

    await edit_message(update, text, keyboard)


async def edit_client(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    client_name = update.callback_query.data[len("edit_client:"):]

    text = f"ℹ Currently editing client <b>{client_name}</b>"
    keyboard = utils.Keyboards.ClientManager.edit_client(client_name)

    await edit_message(update, text, keyboard)


# ////////////////////////////////////////////////////////////////////////////////////////////////
# Editing client name
# ////////////////////////////////////////////////////////////////////////////////////////////////
async def start_edit_client_name_conv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    client_name = update.callback_query.data[len("start_edit_client_name_conv:"):]
    context.user_data["user"].client_to_edit = context.user_data["user"].find_client_by_name(client_name)

    text = f"✅ Editing name for client <b>{context.user_data['user'].client_to_edit.name}</b>\n\nEnter your desired name:"
    keyboard = utils.Keyboards.EditClientName.end_conv

    await edit_message(update, text, keyboard)

    return "edit_client_name_conv.states.name"


async def edit_client_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_name = update.message.text.strip()
    # If the client name is empty
    if new_name == "":
        text = f"❕ Client name was left empty. Please enter a valid name."
        keyboard = utils.Keyboards.EditClientName.end_conv
        await send_message(context, update, text, keyboard)

        return "edit_client_name_conv.states.name"
    # If the client name already exists
    elif context.user_data["user"].client_name_exists(new_name):
        text = f"❕ Client with name {new_name} already exists. Please enter a different name."
        keyboard = utils.Keyboards.EditClientName.end_conv
        await send_message(context, update, text, keyboard)

        return "edit_client_name_conv.states.name"
    else:
        text = f"✅ Client name successfully changed to <b>{new_name}</b>"
        keyboard = utils.Keyboards.back_to_main

        old_name = context.user_data["user"].client_to_edit.name
        context.user_data["user"].client_to_edit.name = new_name
        context.user_data["user"].client_to_edit = None

        await send_message(context, update, text, keyboard)
        return ConversationHandler.END


async def end_edit_client_name_conv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    text = "❌ Edit client operation canceled."
    keyboard = utils.Keyboards.back_to_main

    context.user_data["user"].client_to_edit = None

    await edit_message(update, text, keyboard)
    return ConversationHandler.END


# /////////////////////////////////////////////////////////////////////////////////
# Editing client exchange information
# /////////////////////////////////////////////////////////////////////////////////
async def start_edit_client_exchange_conv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    client_name = update.callback_query.data[len("start_edit_client_api_info_conv:"):]
    context.user_data["user"].new_client = Client()
    context.user_data["user"].new_client.name = client_name

    text = f"✅ Editing exchange information for client <b>{context.user_data['user'].new_client.name}</b>\n\nSelect your exchange:"
    keyboard = utils.Keyboards.EditClientExchange.exchange

    await edit_message(update, text, keyboard)

    return "edit_client_exchange_conv.states.exchange"


async def edit_client_exchange(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    new_exchange = update.callback_query.data[len("edit_client_exchange:"):]
    context.user_data["user"].new_client.exchange_id = new_exchange

    text = f"✅ Exchange <b>{new_exchange}</b> selected.\n\nSelect your account type:"
    keyboard = utils.Keyboards.EditClientExchange.account_type

    await edit_message(update, text, keyboard)

    return "edit_client_exchange_conv.states.account_type"


async def edit_client_account_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    new_account_type = update.callback_query.data[len("edit_client_account_type:"):]
    context.user_data["user"].new_client.account_type = new_account_type

    text = f"✅ Exchange information for client  <b>{context.user_data['user'].new_client.name}</b> will be changed to:\n\n" \
           f"<b>Exchange</b>: {context.user_data['user'].new_client.exchange_id}\n" \
           f"<b>Account type</b>: {context.user_data['user'].new_client.account_type}\n\n" \
           f"Type /confirm to consolidate changes."
    keyboard = utils.Keyboards.EditClientExchange.end_conv

    await edit_message(update, text, keyboard)

    return "edit_client_exchange_conv.states.confirm"


async def confirm_exchange(update: Update, context: ContextTypes.DEFAULT_TYPE):
    client_to_edit = context.user_data["user"].find_client_by_name(context.user_data["user"].new_client.name)
    new_client = context.user_data["user"].new_client

    text = f"✅ Successfully changed exchange information for client {client_to_edit.name}"
    keyboard = utils.Keyboards.back_to_main

    client_to_edit.exchange_id = new_client.exchange_id
    client_to_edit.account_type = new_client.account_type

    context.user_data["user"].new_client = None

    await send_message(context, update, text, keyboard)

    return ConversationHandler.END


async def end_edit_client_exchange_conv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    text = "❌ Edit client operation canceled."
    keyboard = utils.Keyboards.back_to_main

    await edit_message(update, text, keyboard)
    context.user_data["user"].new_client = None

    return ConversationHandler.END


# /////////////////////////////////////////////////////////////////////////////////
# Editing API information for client
# /////////////////////////////////////////////////////////////////////////////////
async def start_edit_client_api_info_conv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    client_name = update.callback_query.data[len("start_edit_client_api_info_conv:"):]
    context.user_data["user"].new_client = Client()
    context.user_data["user"].new_client.name = client_name

    text = f"✅ Editing API information for client <b>{client_name}</b>\n\nEnter the new API key:"
    keyboard = utils.Keyboards.EditClientAPI.end_conv

    await edit_message(update, text, keyboard)

    return "edit_client_api_info_conv.states.api_key"


async def edit_client_api_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_api_key = update.message.text.strip()

    keyboard = utils.Keyboards.EditClientAPI.end_conv
    if new_api_key == "":
        text = f"❕ API key can't be empty. Please re-enter the API info."
        await send_message(context, update, text, keyboard)

        return "edit_client_api_info_conv.states.api_key"
    else:
        context.user_data["user"].new_client.api_key = new_api_key

        text = f"✅ You have entered new API key <b>{new_api_key}</b> for client <b>{context.user_data['user'].new_client.name}</b>\n\nNow enter the new secret key."
        await send_message(context, update, text, keyboard)
        return "edit_client_api_info_conv.states.secret_key"


async def edit_client_secret_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_secret_key = update.message.text.strip()

    keyboard = utils.Keyboards.EditClientAPI.end_conv
    if new_secret_key == "":
        text = f"❕ Secret key can't be empty. Please re-enter the API info."
        await send_message(context, update, text, keyboard)

        return "edit_client_api_info_conv.states.secret_key"
    else:
        context.user_data["user"].new_client.secret_key = new_secret_key

        text = f"✅ You have entered new secret key <b>{new_secret_key}</b> for client <b>{context.user_data['user'].new_client.name}</b>\n\nType /confirm to consolidate the change."
        await send_message(context, update, text, keyboard)
        return "edit_client_api_info_conv.states.confirm"


async def confirm_api_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    client_to_edit = context.user_data["user"].find_client_by_name(context.user_data["user"].new_client.name)
    new_client = context.user_data["user"].new_client

    text = f"✅ Successfully changed API information for client {client_to_edit.name}"
    keyboard = utils.Keyboards.back_to_main

    client_to_edit.api_key = new_client.api_key
    client_to_edit.secret_key = new_client.secret_key

    context.user_data["user"].new_client = None

    await send_message(context, update, text, keyboard)
    return ConversationHandler.END


async def end_edit_client_api_info_conv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    text = "❌ Edit client operation canceled."
    keyboard = utils.Keyboards.back_to_main

    await edit_message(update, text, keyboard)
    context.user_data["user"].new_client = None

    return ConversationHandler.END


# ////////////////////////////////////////////////////////////////////////////////////////////////
# Removing client from client list
# ////////////////////////////////////////////////////////////////////////////////////////////////
async def start_remove_client_conv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    client_name = update.callback_query.data[len("start_remove_client_conv:"):]
    context.user_data["user"].client_to_edit = context.user_data["user"].find_client_by_name(client_name)

    text = f"🗑 Type /confirm to confirm the deletion of client <b>{client_name}</b>\n\n<b>❗ (This action is irreversible)</b> ❗"
    keyboard = utils.Keyboards.RemoveClient.end_conv

    await edit_message(update, text, keyboard)

    return "remove_client_conv.states.confirm"


async def confirm_client_removal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    client_name = context.user_data["user"].client_to_edit.name
    context.user_data["user"].remove_client(client_name)

    text = f"✅ Client {client_name} removed."
    keyboard = utils.Keyboards.back_to_main

    context.user_data["user"].client_to_edit = None

    await send_message(context, update, text, keyboard)
    return ConversationHandler.END


async def end_remove_client_conv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    text = "❌ Remove client operation canceled."
    keyboard = utils.Keyboards.back_to_main

    context.user_data["user"].client_to_edit = None

    await edit_message(update, text, keyboard)
    return ConversationHandler.END
