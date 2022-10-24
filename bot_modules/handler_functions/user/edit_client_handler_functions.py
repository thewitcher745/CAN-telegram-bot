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
        keyboard = utils.Keyboards.manage_clients(client_name_list)
    else:
        text = "🟢 <b>Client manager menu</b>\n\nYou don't have any clients to edit. Add new clients first through main menu or the button below."
        keyboard = utils.Keyboards.manage_clients_empty

    await edit_message(update, text, keyboard)


async def edit_client(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    client_name = update.callback_query.data[len("edit_client:"):]

    text = f"ℹ Currently editing client <b>{client_name}</b>"
    keyboard = utils.Keyboards.edit_client(client_name)

    await edit_message(update, text, keyboard)


# ////////////////////////////////////////////////////////////////////////////////////////////////
# Editing client name
# ////////////////////////////////////////////////////////////////////////////////////////////////
async def start_edit_client_name_conv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    client_name = update.callback_query.data[len("start_edit_client_name_conv:"):]
    context.user_data["editing_client"] = client_name

    text = f"✅ Editing name for client <b>{client_name}</b>\n\nEnter your desired name:"
    keyboard = utils.Keyboards.end_client_name_conv

    await edit_message(update, text, keyboard)

    return "edit_client_name_conv.name"


async def edit_client_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_name = update.message.text
    text = f"✅ Client name successfully changed from {context.user_data['editing_client']} to <b>{new_name}</b>"
    keyboard = utils.Keyboards.back_to_main

    context.user_data["clients"][new_name] = context.user_data["clients"][context.user_data["editing_client"]]
    del context.user_data["clients"][context.user_data["editing_client"]]

    await send_message(context, update, text, keyboard)
    return ConversationHandler.END


async def end_edit_client_name_conv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    text = "❌ Operation canceled."
    keyboard = utils.Keyboards.back_to_main

    await send_message(context, update, text, keyboard)
    return ConversationHandler.END


# /////////////////////////////////////////////////////////////////////////////////
# Editing API information for client
# /////////////////////////////////////////////////////////////////////////////////
async def start_edit_client_api_info_conv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    client_name = update.callback_query.data[len("start_edit_client_api_info_conv:"):]
    context.user_data["editing_client"] = client_name

    text = f"✅ Editing API information for client <b>{client_name}</b>\n\nEnter the new API key:"
    keyboard = utils.Keyboards.end_client_api_info_conv

    await edit_message(update, text, keyboard)

    return "edit_client_api_info_conv.api_key"


async def edit_client_api_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["new_api_key"] = update.message.text
    text = f"✅ You have entered new API key <b>{context.user_data['new_api_key']}</b> for client <b>{context.user_data['editing_client']}</b>\n\nNow enter the new secret key."
    keyboard = utils.Keyboards.end_client_api_info_conv

    await send_message(context, update, text, keyboard)
    return "edit_client_api_info_conv.secret_key"


async def edit_client_secret_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["new_secret_key"] = update.message.text
    text = f"✅ You have entered new secret key <b>{context.user_data['new_api_key']}</b> for client <b>{context.user_data['editing_client']}</b>\n\nType /confirm to consolidate the change."

    keyboard = utils.Keyboards.end_client_api_info_conv

    await send_message(context, update, text, keyboard)
    return "edit_client_api_info_conv.confirm"


async def confirm_api_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    client_name = context.user_data['editing_client']
    text = f"✅ Successfully changed API information for client {context.user_data['editing_client']}"
    keyboard = utils.Keyboards.back_to_main
    print(context.user_data["clients"])
    context.user_data["clients"][client_name]["api_key"] = context.user_data["new_api_key"]
    context.user_data["clients"][client_name]["secret_key"] = context.user_data["new_secret_key"]
    del context.user_data["new_api_key"]
    del context.user_data["new_secret_key"]

    await send_message(context, update, text, keyboard)
    return ConversationHandler.END


async def end_edit_client_api_info_conv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    text = "❌ Operation canceled."
    keyboard = utils.Keyboards.back_to_main

    await send_message(context, update, text, keyboard)
    return ConversationHandler.END


# ////////////////////////////////////////////////////////////////////////////////////////////////
# Removing client from client list
# ////////////////////////////////////////////////////////////////////////////////////////////////
async def remove_client(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    client_name = update.callback_query.data[len("remove_client:"):]
    print(client_name)
    print(context.user_data["clients"])
    del context.user_data["clients"][client_name]
    print(context.user_data["clients"])
    text = f"🗑 Client <b>{client_name} successfully removed.</b>"
    keyboard = utils.Keyboards.back_to_main

    await edit_message(update, text, keyboard)
