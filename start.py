import logging

from dotenv import dotenv_values
from telegram.ext import (
    ApplicationBuilder,
    PicklePersistence,
)

from bot_modules import handlers

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    persistence = PicklePersistence(filepath="persistence_file.pickle")
    application = (
        ApplicationBuilder()
        .token(dotenv_values(".env")["BOT_AUTH_TOKEN"])
        .persistence(persistence)
        .build()
    )
    handlers = [
        handlers.start_handler,

        handlers.add_client_conv_handler,

        handlers.client_manager_handler,
        handlers.client_manager_name_handler,
        handlers.remove_client_handler,
        handlers.edit_client_name_handler,
        handlers.edit_client_api_info_handler,
        handlers.edit_client_exchange_handler,

        handlers.fetch_user_api_data_handler,
        handlers.fetch_balance_handler,
        handlers.signal_handler,
        handlers.back_to_main_handler,
        handlers.check_api_connection_handler,

    ]

    for handler in handlers:
        application.add_handler(handler)

    application.run_polling()
