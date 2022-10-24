from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    filters,
)

from bot_modules.handler_functions import exchange_handler_functions, menu_handler_functions
from bot_modules.handler_functions.user import client_conv_handler_functions, edit_client_handler_functions

start_handler = CommandHandler("start", menu_handler_functions.main_menu)

client_manager_handler = CallbackQueryHandler(
    edit_client_handler_functions.client_manager, pattern="client_manager"
)

client_manager_name_handler = CallbackQueryHandler(
    edit_client_handler_functions.edit_client, pattern=r"^edit_client:.*"
)

edit_client_name_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(
        edit_client_handler_functions.start_edit_client_name_conv, pattern=r"^start_edit_client_name_conv:.*"
    )],
    states={
        "edit_client_name_conv.name": [MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            edit_client_handler_functions.edit_client_name,
        )]
    },
    fallbacks=[
        CommandHandler("end", edit_client_handler_functions.end_edit_client_name_conv),
        CallbackQueryHandler(
            edit_client_handler_functions.end_edit_client_name_conv, pattern="end_edit_client_name_conv"
        ),
    ])

edit_client_api_info_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(
        edit_client_handler_functions.start_edit_client_api_info_conv, pattern=r"^start_edit_client_api_info_conv:.*"
    )],
    states={
        "edit_client_api_info_conv.api_key": [MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            edit_client_handler_functions.edit_client_api_key,
        )],
        "edit_client_api_info_conv.secret_key": [MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            edit_client_handler_functions.edit_client_secret_key,
        )],
        "edit_client_api_info_conv.confirm": [CommandHandler(
            "confirm",
            edit_client_handler_functions.confirm_api_info,
        )]
    },
    fallbacks=[
        CommandHandler("end", edit_client_handler_functions.end_edit_client_api_info_conv),
        CallbackQueryHandler(
            edit_client_handler_functions.end_edit_client_api_info_conv, pattern="end_edit_client_api_info_conv"
        ),
    ])

remove_client_handler = CallbackQueryHandler(
    edit_client_handler_functions.remove_client, pattern=r"^remove_client:.*"
)

fetch_user_api_data_handler = CallbackQueryHandler(
    exchange_handler_functions.fetch_user_portfolio, pattern="fetch_user_api_info"
)

fetch_balance_handler = CallbackQueryHandler(
    exchange_handler_functions.fetch_user_portfolio, pattern="fetch_user_portfolio"
)

back_to_main_handler = CallbackQueryHandler(
    menu_handler_functions.main_menu, pattern="back_to_main"
)

check_api_connection_handler = CallbackQueryHandler(
    exchange_handler_functions.check_api_connection, pattern="check_api_connection"
)

client_conv_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            client_conv_handler_functions.start_new_client_conv,
            pattern="start_new_client_conv",
        ),
    ],
    states={
        "client_conv.states.client_name": [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                client_conv_handler_functions.get_custom_client_name,
            ),
            CallbackQueryHandler(
                client_conv_handler_functions.accept_default_client_name,
                pattern="accept_default_client_name",
            ),
        ],
        "client_conv.states.client_api_key": [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                client_conv_handler_functions.get_client_api_key,
            )
        ],
        "client_conv.states.client_secret_key": [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                client_conv_handler_functions.get_client_secret_key,
            )
        ],
        "client_conv.states.confirm": [
            CommandHandler("confirm", client_conv_handler_functions.confirm_client_info)
        ],
    },
    fallbacks=[
        CommandHandler("end", client_conv_handler_functions.end_new_client_conv),
        CallbackQueryHandler(
            client_conv_handler_functions.end_new_client_conv, pattern="end_new_client_conv"
        ),
    ],
)

signal_handler = MessageHandler(
    filters.FORWARDED, exchange_handler_functions.process_signal
)