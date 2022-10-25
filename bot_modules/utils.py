import re

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode


async def send_message(context, update, text, keyboard=None):
    if keyboard is None:
        keyboard = []
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode("HTML"),
    )


async def edit_message(update, text, keyboard=None):
    if keyboard is None:
        keyboard = []
    await update.callback_query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode("HTML"),
    )


def signal_regex(text):
    symbols = re.split(r"(\w{3,}/\w{3,})", text)[1]
    exchanges = re.split(r"Exchanges: (.{3,})", text)[1]
    signal_type = re.split(r"Signal Type: (.+)", text)[1]
    leverage = re.split(r"Leverage: (.+)", text)[1]
    amount = re.split(r"Amount: (.+)", text)[1]
    entry_targets = targets_deconstructor(
        re.split(r"Entry Targets:\n([0-9).\s]+).*\n\n", text)[1]
    )
    take_profit_targets = targets_deconstructor(
        re.split(r"Take-Profit Targets:\n([0-9).\s]+).*\n\n", text)[1]
    )
    stop_targets = targets_deconstructor(
        re.split(r"Stop Targets:\n([0-9).\s]+).*\n\n", text)[1]
    )
    trailing_config = config_deconstructor(
        re.split(r"Trailing Configuration:\n([\S\s]+).*\n\n", text)[1]
    )

    return [
        symbols,
        exchanges,
        signal_type,
        leverage,
        amount,
        entry_targets,
        take_profit_targets,
        stop_targets,
        trailing_config,
    ]


def targets_deconstructor(string):
    target_list = re.finditer(r"(\d)\)\s([0-9]+\.[0-9]+)", string)
    return list([float(target.groups()[1]) for target in target_list])


def config_deconstructor(string):
    stop = re.split(r"Stop:\s(\w+)", string)[1]
    trigger = re.split(r"Trigger:\s([\w()\s0-9]+)", string)[1]
    return [stop, trigger]


def check_user_auth(context):
    if "api_key" in context.user_data and "secret_key" in context.user_data:
        return True
    return False


def fetch_user_client_list(context):
    try:
        return context.user_data["clients"].keys()
    except KeyError:
        return []


class Buttons:
    class AddClient:
        add_new_client = InlineKeyboardButton(
            "➕ Add new client", callback_data="start_new_client_conv"
        )
        accept_default_client_name = InlineKeyboardButton(
            "✅ Accept default name", callback_data="accept_default_client_name"
        )
        end_conv = InlineKeyboardButton(
            "❌ End operation", callback_data="end_new_client_conv"
        )

    class ClientManager:
        client_manager = InlineKeyboardButton(
            "📝 Client manager", callback_data="client_manager"
        )

        @staticmethod
        def client_to_modify(name):
            return InlineKeyboardButton(
                f"⭕ {name}", callback_data=f"edit_client:{name}"
            )

    class EditClientName:
        end_conv = InlineKeyboardButton(
            "❌ End operation", callback_data="end_edit_client_name_conv"
        )

        @staticmethod
        def edit_client_name(client_name):
            return InlineKeyboardButton(
                "🖊 Edit client name", callback_data=f"start_edit_client_name_conv:{client_name}"
            )

    class EditClientAPI:
        end_conv = InlineKeyboardButton(
            "❌ End operation", callback_data="end_edit_client_api_info_conv"
        )

        @staticmethod
        def edit_client_api_info(client_name):
            return InlineKeyboardButton(
                "🖊 Edit client API info", callback_data=f"start_edit_client_api_info_conv:{client_name}"
            )

    class RemoveClient:
        end_conv = InlineKeyboardButton(
            "❌ End operation", callback_data="end_remove_client_conv"
        )

        @staticmethod
        def remove_client(client_name):
            return InlineKeyboardButton(
                "🗑 Remove client", callback_data=f"start_remove_client_conv:{client_name}"
            )

    portfolio = InlineKeyboardButton(
        "💵 Portfolio", callback_data="fetch_user_portfolio"
    )
    check_api_connection = InlineKeyboardButton(
        "💻 Check connection to exchange", callback_data="check_api_connection"
    )
    back_to_main = InlineKeyboardButton(
        "↩ Back to main menu", callback_data="back_to_main"
    )

    @staticmethod
    def previous_menu(callback_data):
        return InlineKeyboardButton(
            f"⬆ Back", callback_data=f"{callback_data}"
        )


class Keyboards:
    class AddClient:
        new_client_name = [
            [Buttons.AddClient.accept_default_client_name],
            [Buttons.AddClient.end_conv],
        ]
        end_conv = [[Buttons.AddClient.end_conv]]

    class ClientManager:
        manage_clients_empty = [
            [Buttons.AddClient.add_new_client],
            [Buttons.back_to_main],
        ]

        @staticmethod
        def manage_clients(client_name_list):
            keyboard = []
            row = []

            for i, client_name in enumerate(client_name_list):
                row.append(Buttons.ClientManager.client_to_modify(client_name))

                if i % 2 == 1:
                    keyboard.append(row)
                    row = []
            keyboard.append(row)
            keyboard.extend(Keyboards.back_to_main)
            return keyboard

        @staticmethod
        def edit_client(client_name):
            keyboard = [[Buttons.EditClientAPI.edit_client_api_info(client_name),
                         Buttons.EditClientName.edit_client_name(client_name)],
                        [Buttons.RemoveClient.remove_client(client_name)],
                        [Buttons.back_to_main, Buttons.previous_menu("client_manager")]]

            return keyboard

    class EditClientName:
        end_conv = [[Buttons.EditClientName.end_conv]]

    class EditClientAPI:
        end_conv = [[Buttons.EditClientAPI.end_conv]]

    class RemoveClient:
        end_conv = [[Buttons.RemoveClient.end_conv]]

    main_menu = [
        [Buttons.AddClient.add_new_client, Buttons.ClientManager.client_manager],
        [Buttons.portfolio],
        [Buttons.check_api_connection],
    ]

    back_to_main = [[Buttons.back_to_main]]

    portfolio_no_clients = [
        [Buttons.AddClient.add_new_client],
        [Buttons.back_to_main],
    ]
