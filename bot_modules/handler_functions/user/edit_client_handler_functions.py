from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot_modules import utils

send_message = utils.send_message
edit_message = utils.edit_message


async def client_manager(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    client_name_list = utils.fetch_user_client_list(context)
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

    context.user_data["client_to_edit"] = client_name

    text = f"✅ Editing name for client <b>{client_name}</b>\n\nEnter your desired name:"
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
    elif new_name in context.user_data["clients"].keys():
        text = f"❕ Client with name {new_name} already exists. Please enter a different name."
        keyboard = utils.Keyboards.EditClientName.end_conv
        await send_message(context, update, text, keyboard)

        return "edit_client_name_conv.states.name"
    else:
        text = f"✅ Client name successfully changed from {context.user_data['client_to_edit']} to <b>{new_name}</b>"
        keyboard = utils.Keyboards.back_to_main

        context.user_data["clients"][new_name] = context.user_data["clients"][context.user_data["client_to_edit"]]
        del context.user_data["clients"][context.user_data["client_to_edit"]]
        del context.user_data["client_to_edit"]

        await send_message(context, update, text, keyboard)
        return ConversationHandler.END


async def end_edit_client_name_conv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    text = "❌ Edit client operation canceled."
    keyboard = utils.Keyboards.back_to_main

    del context.user_data["client_to_edit"]

    await edit_message(update, text, keyboard)
    return ConversationHandler.END


# /////////////////////////////////////////////////////////////////////////////////
# Editing API information for client
# /////////////////////////////////////////////////////////////////////////////////
async def start_edit_client_api_info_conv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    client_name = update.callback_query.data[len("start_edit_client_api_info_conv:"):]
    context.user_data["client_to_edit"] = client_name

    text = f"✅ Editing API information for client <b>{client_name}</b>\n\nEnter the new API key:"
    keyboard = utils.Keyboards.EditClientAPI.end_conv

    await edit_message(update, text, keyboard)

    return "edit_client_api_info_conv.states.api_key"


async def edit_client_api_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["new_api_key"] = update.message.text.strip()

    keyboard = utils.Keyboards.EditClientAPI.end_conv
    if context.user_data["new_api_key"] == "":
        text = f"❕ API key can't be empty. Please re-enter the API info."
        await send_message(context, update, text, keyboard)

        return "edit_client_api_info_conv.states.api_key"
    else:
        text = f"✅ You have entered new API key <b>{context.user_data['new_api_key']}</b> for client <b>{context.user_data['client_to_edit']}</b>\n\nNow enter the new secret key."
        await send_message(context, update, text, keyboard)
        return "edit_client_api_info_conv.states.secret_key"


async def edit_client_secret_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["new_secret_key"] = update.message.text.strip()

    keyboard = utils.Keyboards.EditClientAPI.end_conv
    if context.user_data["new_secret_key"] == "":
        text = f"❕ Secret key can't be empty. Please re-enter the API info."
        await send_message(context, update, text, keyboard)

        return "edit_client_api_info_conv.states.secret_key"
    else:
        text = f"✅ You have entered new secret key <b>{context.user_data['new_api_key']}</b> for client <b>{context.user_data['client_to_edit']}</b>\n\nType /confirm to consolidate the change."
        await send_message(context, update, text, keyboard)
        return "edit_client_api_info_conv.states.confirm"


async def confirm_api_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    client_name = context.user_data['client_to_edit']
    text = f"✅ Successfully changed API information for client {context.user_data['client_to_edit']}"
    keyboard = utils.Keyboards.back_to_main

    context.user_data["clients"][client_name]["api_key"] = context.user_data["new_api_key"]
    context.user_data["clients"][client_name]["secret_key"] = context.user_data["new_secret_key"]
    del context.user_data["new_api_key"]
    del context.user_data["new_secret_key"]
    del context.user_data["client_to_edit"]

    await send_message(context, update, text, keyboard)
    return ConversationHandler.END


async def end_edit_client_api_info_conv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    text = "❌ Edit client operation canceled."
    keyboard = utils.Keyboards.back_to_main

    await edit_message(update, text, keyboard)
    del context.user_data["client_to_edit"]

    return ConversationHandler.END


# ////////////////////////////////////////////////////////////////////////////////////////////////
# Removing client from client list
# ////////////////////////////////////////////////////////////////////////////////////////////////
async def start_remove_client_conv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    client_name = update.callback_query.data[len("start_remove_client_conv:"):]
    context.user_data["client_to_remove"] = client_name

    text = f"🗑 Type /confirm to confirm the deletion of client <b>{client_name}</b>\n\n<b>❗ (This action is irreversible)</b> ❗"
    keyboard = utils.Keyboards.RemoveClient.end_conv

    await edit_message(update, text, keyboard)

    return "remove_client_conv.states.confirm"


async def confirm_client_removal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    client_name = context.user_data['client_to_remove']

    text = f"✅ Client {context.user_data['client_to_remove']} removed."
    keyboard = utils.Keyboards.back_to_main
    del context.user_data["clients"][client_name]
    del context.user_data["client_to_remove"]

    await send_message(context, update, text, keyboard)
    return ConversationHandler.END


async def end_remove_client_conv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    text = "❌ Remove client operation canceled."
    keyboard = utils.Keyboards.back_to_main

    del context.user_data["client_to_remove"]

    await edit_message(update, text, keyboard)
    return ConversationHandler.END
