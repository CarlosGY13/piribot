from dataclasses import dataclass
from typing import Literal
import os

from dotenv import load_dotenv

# Auto-load .env only for local/development.
# In production, environment variables should be set directly.
load_dotenv()

LanguageCode = Literal["es", "qu", "shp"]


@dataclass
class Settings:
    """
    Container for Piribot's main configuration.

    Attributes:
        telegram_bot_token: Telegram bot token.
        gemini_api_key: API key to access Gemini.
        default_language: Default bot language (es, qu or shp).
    """
    telegram_bot_token: str
    gemini_api_key: str
    default_language: LanguageCode


def _read_env_var(name: str) -> str:
    """
    Read a required environment variable.

    Inputs:
        name: Environment variable name.
    Outputs:
        Value of the variable, or raises RuntimeError if not defined.
    """
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"La variable de entorno {name} es obligatoria pero no está definida."
        )
    return value


def load_settings() -> Settings:
    """
    Load and validate required environment variables.

    Inputs:
        - None (reads from `os.environ`).
    Outputs:
        - Settings instance with validated values.
    """
    telegram_bot_token = _read_env_var("TELEGRAM_BOT_TOKEN")
    gemini_api_key = _read_env_var("GEMINI_API_KEY")
    default_language = os.getenv("PIRIBOT_DEFAULT_LANGUAGE", "es").lower()

    if default_language not in ("es", "qu", "shp"):
        # Safe fallback
        default_language = "es"

    return Settings(
        telegram_bot_token=telegram_bot_token,
        gemini_api_key=gemini_api_key,
        default_language=default_language,  # type: ignore[arg-type]
    )

settings = load_settings()


