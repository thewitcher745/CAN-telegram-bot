from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    filters,
)

from bot_modules.handler_functions import exchange_handler_functions, menu_handler_functions
from bot_modules.handler_functions.user import add_client_conv_handler_functions, edit_client_handler_functions

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
        "edit_client_name_conv.states.name": [MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            edit_client_handler_functions.edit_client_name,
        )]
    },
    fallbacks=[
        CallbackQueryHandler(
            edit_client_handler_functions.end_edit_client_name_conv, pattern="end_edit_client_name_conv"
        ),
    ])

edit_client_api_info_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(
        edit_client_handler_functions.start_edit_client_api_info_conv, pattern=r"^start_edit_client_api_info_conv:.*"
    )],
    states={
        "edit_client_api_info_conv.states.api_key": [MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            edit_client_handler_functions.edit_client_api_key,
        )],
        "edit_client_api_info_conv.states.secret_key": [MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            edit_client_handler_functions.edit_client_secret_key,
        )],
        "edit_client_api_info_conv.states.confirm": [CommandHandler(
            "confirm",
            edit_client_handler_functions.confirm_api_info,
        )]
    },
    fallbacks=[
        CallbackQueryHandler(
            edit_client_handler_functions.end_remove_client_conv, pattern="end_remove_client_conv"
        ),
    ])

remove_client_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(edit_client_handler_functions.start_remove_client_conv,
                             pattern=r"^start_remove_client_conv:.*")
    ],
    states={
        "remove_client_conv.states.confirm": [
            CommandHandler(
                "confirm", edit_client_handler_functions.confirm_client_removal)
        ],
    },
    fallbacks=[
        CallbackQueryHandler(
            edit_client_handler_functions.end_remove_client_conv, pattern="end_remove_client_conv"
        )]
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

add_client_conv_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            add_client_conv_handler_functions.start_new_client_conv,
            pattern="start_new_client_conv",
        ),
    ],
    states={
        "add_client_conv.states.client_name": [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                add_client_conv_handler_functions.get_custom_client_name,
            ),
            CallbackQueryHandler(
                add_client_conv_handler_functions.accept_default_client_name,
                pattern="accept_default_client_name",
            ),
        ],
        "add_client_conv.states.client_api_key": [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                add_client_conv_handler_functions.get_client_api_key,
            )
        ],
        "add_client_conv.states.client_secret_key": [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                add_client_conv_handler_functions.get_client_secret_key,
            )
        ],
        "add_client_conv.states.confirm": [
            CommandHandler("confirm", add_client_conv_handler_functions.confirm_client_info)
        ],
    },
    fallbacks=[
        CommandHandler("end", add_client_conv_handler_functions.end_new_client_conv),
        CallbackQueryHandler(
            add_client_conv_handler_functions.end_new_client_conv, pattern="end_new_client_conv"
        ),
    ],
)

signal_handler = MessageHandler(
    filters.FORWARDED, exchange_handler_functions.process_signal
)
