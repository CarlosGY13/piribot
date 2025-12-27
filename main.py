import logging

from bot.telegram_bot import create_application
from config.settings import settings


def main() -> None:
    """
    Initialize logging and start the Piribot Telegram bot.

    Inputs:
        - No parameters; configuration is read from `config.settings`.
    Outputs:
        - None. Keeps the process running via `run_polling()`.
    """
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    application = create_application(settings.telegram_bot_token)
    logging.getLogger(__name__).info("Starting Piribot...")
    application.run_polling(
        allowed_updates=["message"],
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()


