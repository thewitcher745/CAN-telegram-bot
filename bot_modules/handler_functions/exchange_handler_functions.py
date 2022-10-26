from ccxt.base.errors import AuthenticationError
from telegram import Update
from telegram.ext import ContextTypes

from api_connections import api_master
from bot_modules import utils

edit_message = utils.edit_message
send_message = utils.send_message
signal_regex = utils.signal_regex


async def process_signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    [
        symbols,
        exchanges,
        signal_type,
        leverage,
        amount,
        entry_targets,
        take_profit_targets,
        stop_targets,
        trailing_config,
    ] = signal_regex(text)

    output_text = f'Received signal with symbol {symbols} for exchange {exchanges}, signal type is {signal_type} and ' \
                  f'leverage is {leverage} with amount equal to {amount} '
    output_text += f'\n\nEntry targets: {entry_targets}\nTake profit targets: {take_profit_targets}\nStop targets: {stop_targets}'
    output_text += f'\n\nTrailing configuration: {trailing_config}'


async def fetch_user_portfolio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    loading_text = (
        "⌛ Loading portfolio, this can take a bit if you have many clients added..."
    )
    await edit_message(update, loading_text)

    keyboard = utils.Keyboards.back_to_main
    client_name_list = utils.fetch_user_client_list(context)

    if len(client_name_list) > 0:
        text = ""
        for client_name in client_name_list:
            try:
                exchange = context.user_data["clients"][client_name]["exchange"]
                api_master.Exchange()

                balances = exchange.api_fetch_client_balance()
                text += f"<b>{client_name}</b>\n💵 Total wallet balance ({round(balances['totalWalletBalance'][1], 6)}BTC = {round(balances['totalWalletBalance'][0], 3)}USDT)\n\n"

            except AuthenticationError:
                text += f"<b>{client_name}</b>\n❌ Logging in to exchange failed using the provided API and secret " \
                        f"keys. Please check if they are valid.\n\n "

    else:
        text = f"❌ No clients were found! Try adding some through the main menu or the button below."
        keyboard = utils.Keyboards.portfolio_no_clients

    await edit_message(update, text, keyboard)


async def check_api_connection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    loading_text = "⌛ Loading, this can take a bit if you have many clients added..."
    keyboard = utils.Keyboards.back_to_main
    await edit_message(update, loading_text)

    client_name_list = utils.fetch_user_client_list(context)

    if len(client_name_list) > 0:
        text = ""
        for client_name in client_name_list:
            exchange = context.user_data["clients"][client_name]["exchange"]
            api_master.Exchange()
            check_result = exchange.api_check_api_connection()

            if check_result == "Success":
                text += f"✅ <b>{client_name}</b>\n API is accessible and credentials are correct.\n\n"
            elif check_result == "AuthError":
                text += f"❌ <b>{client_name}</b>\n API is accessible, but the API key and/or secret don't seem to work.\n\n"
            else:
                text += f"❌ <b>{client_name}</b>\n API is inaccessible, this can be due to a server issue from the exchange or the bot's server being unable to connect to the exchange. Contact the admins.\n\n"
    else:
        text = f"❌ No clients were found! Try adding some through the main menu or the button below."
        keyboard = utils.Keyboards.portfolio_no_clients

    await edit_message(update, text, keyboard)
