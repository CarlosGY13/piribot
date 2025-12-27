import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from config.settings import settings, LanguageCode
from bot.language import LANG_LABELS, LANG_CODES_BY_LABEL, get_message, get_disclaimer
from bot.gemini_client import generate_response

logger = logging.getLogger(__name__)


def _build_language_keyboard() -> ReplyKeyboardMarkup:
    """
    Build the language selection keyboard.

    Inputs:
        - None (uses labels from `LANG_LABELS`).
    Outputs:
        - ReplyKeyboardMarkup ready to be sent in Telegram.
    """
    labels = [LANG_LABELS["es"], LANG_LABELS["qu"], LANG_LABELS["shp"]]
    keyboard = [[labels[0]], [labels[1]], [labels[2]]]
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def _load_alerts_config() -> Dict[str, Any]:
    """
    Load basic alerts configuration from disk.

    Inputs:
        - None (reads `data/alerts.json` relative to the project).
    Outputs:
        - Dictionary with keywords and alert messages per language.
    """
    base_dir = Path(__file__).resolve().parents[1]
    alerts_path = base_dir / "data" / "alerts.json"

    if not alerts_path.exists():
        logger.warning("No se encontró alerts.json, no se harán detecciones locales de alerta.")
        return {}

    try:
        with alerts_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:  # pragma: no cover - lectura simple de archivo
        logger.error("Error al leer alerts.json: %s", exc)
        return {}


_ALERTS_CONFIG = _load_alerts_config()


def _detect_alert_message(
    text: str,
    language: LanguageCode,
) -> Optional[str]:
    """
    Detect whether a text contains potential warning signs.

    Inputs:
        text: Free-form user message.
        language: Current conversation language.
    Outputs:
        - Alert message in the corresponding language, or None if no matches.
    """
    if not _ALERTS_CONFIG:
        return None

    lang_cfg = _ALERTS_CONFIG.get(language) or _ALERTS_CONFIG.get("es")
    if not lang_cfg:
        return None

    keywords = lang_cfg.get("keywords", [])
    alert_message = lang_cfg.get("message", "")

    text_lower = text.lower()
    for kw in keywords:
        if kw.lower() in text_lower:
            return alert_message

    return None


def _get_user_language(
    context: ContextTypes.DEFAULT_TYPE,
) -> LanguageCode:
    """
    Get the current user language from `user_data`.

    Inputs:
        context: python-telegram-bot context for the current user.
    Outputs:
        - Language code ('es', 'qu' or 'shp').
    """
    lang = context.user_data.get("language")
    if lang in ("es", "qu", "shp"):
        return lang  # type: ignore[return-value]
    return settings.default_language


def _set_user_language(
    context: ContextTypes.DEFAULT_TYPE,
    lang: LanguageCode,
) -> None:
    """
    Store the user's preferred language in `user_data`.

    Inputs:
        context: python-telegram-bot context.
        lang: Selected language code.
    Outputs:
        - None (updates `context.user_data` in-place).
    """
    context.user_data["language"] = lang


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /start command.

    Inputs:
        update: Incoming Telegram update.
        context: Bot execution context.
    Outputs:
        - None. Sends welcome message, language keyboard and disclaimer.
    """
    user = update.effective_user
    logger.info("Received /start from user_id=%s", user.id if user else "unknown")

    # Default language until the user chooses another one
    _set_user_language(context, settings.default_language)
    lang = _get_user_language(context)

    welcome = get_message(lang, "welcome")
    choose_lang = get_message(lang, "choose_language")
    disclaimer = get_disclaimer(lang)

    keyboard = _build_language_keyboard()

    if update.message:
        await update.message.reply_text(
            welcome,
            reply_markup=keyboard,
        )
        await update.message.reply_text(
            choose_lang,
            reply_markup=keyboard,
        )
        await update.message.reply_text(
            disclaimer,
            reply_markup=keyboard,
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /help command.

    Inputs:
        update: Incoming Telegram update.
        context: Bot execution context.
    Outputs:
        - None. Sends a message with usage examples.
    """
    lang = _get_user_language(context)
    text = get_message(lang, "help")
    if update.message:
        await update.message.reply_text(text)


async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /language command to show the language selector again.

    Inputs:
        update: Incoming Telegram update.
        context: Bot execution context.
    Outputs:
        - None. Sends the language keyboard.
    """
    lang = _get_user_language(context)
    choose_lang = get_message(lang, "choose_language")
    keyboard = _build_language_keyboard()
    if update.message:
        await update.message.reply_text(
            choose_lang,
            reply_markup=keyboard,
        )


async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle text messages and photos (as text + optional caption).

    Inputs:
        update: Incoming Telegram message (text or photo).
        context: Bot execution context, with `user_data` for memory.
    Outputs:
        - None. Sends the generated reply to the chat.
    """

    if not update.message:
        return

    # If the message has text, use it.
    # If it's a photo without text, use a generic description.
    user_text = (update.message.text or update.message.caption or "").strip()
    if not user_text and update.message.photo:
        user_text = (
            "He enviado una imagen relacionada con un examen o evaluación médica "
            "durante el embarazo. Quisiera una orientación general, sin diagnóstico."
        )
    if not user_text:
        return

    # Is the user trying to select a language using the keyboard?
    if user_text in LANG_CODES_BY_LABEL:
        lang = LANG_CODES_BY_LABEL[user_text]
        _set_user_language(context, lang)
        confirm = get_message(lang, "language_set")
        # Only confirm the language; the full disclaimer was already sent in /start
        await update.message.reply_text(
            confirm,
            reply_markup=ReplyKeyboardRemove(),
        )
        return

    lang = _get_user_language(context)

    # Per-user history to give context to Gemini
    history = context.user_data.get("history") or []

    # Local detection of potential warning signs (only once per conversation)
    alert_message = _detect_alert_message(user_text, lang)
    alert_already_shown = context.user_data.get("alert_shown", False)
    alert_hint = False

    if alert_message and not alert_already_shown:
        await update.message.reply_text(alert_message)
        context.user_data["alert_shown"] = True
        alert_hint = True

    try:
        reply = await generate_response(
            user_message=user_text,
            language=lang,
            alert_hint=alert_hint,
            history=history,
        )

        # Update history (user + bot reply)
        history.append({"role": "user", "text": user_text})
        history.append({"role": "assistant", "text": reply})
        # Limit history size to avoid unbounded growth
        context.user_data["history"] = history[-10:]

        await update.message.reply_text(reply)
    except Exception as exc:  # pragma: no cover - general handling
        logger.error("Error in handle_text_message: %s", exc)
        fallback = get_message(lang, "fallback_error")
        await update.message.reply_text(fallback)


def create_application(telegram_token: str) -> Application:
    """
    Create the main python-telegram-bot `Application` instance.

    Inputs:
        telegram_token: Telegram bot token.
    Outputs:
        - Application object configured with handlers and ready for `run_polling()`.
    """
    application = (
        ApplicationBuilder()
        .token(telegram_token)
        .concurrent_updates(False)
        .build()
    )

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("language", language_command))

    # Text message handler (non-commands)
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_text_message,
        )
    )

    # Basic photo handler: treated as evaluation-related messages,
    # without visually interpreting the image (only general context).
    # For now we reuse `handle_text_message`, reading only the caption.
    # If a different behaviour is needed, a dedicated photo handler can be added.
    application.add_handler(
        MessageHandler(
            filters.PHOTO,
            handle_text_message,
        )
    )

    return application


