import asyncio
import json
import logging
from pathlib import Path
from textwrap import dedent
from typing import Optional

from google import genai

from config.settings import settings, LanguageCode
from bot.prompts import build_system_prompt
from bot.language import get_disclaimer, get_short_disclaimer

logger = logging.getLogger(__name__)

_client = genai.Client(api_key=settings.gemini_api_key)

_GEMINI_MODEL_NAME = "gemini-2.5-flash"


def _load_faq_examples() -> dict:
    """
    Load FAQ examples from disk.

    Inputs:
        - None (reads `data/faq.json` relative to the project).
    Outputs:
        - Dict with Q&A lists per language, or {} on error.
    """
    base_dir = Path(__file__).resolve().parents[1]
    faq_path = base_dir / "data" / "faq.json"
    if not faq_path.exists():
        logger.warning("No se encontró faq.json, el prompt se generará sin ejemplos.")
        return {}

    try:
        with faq_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:  # pragma: no cover - lectura de archivo simple
        logger.error("Error al leer faq.json: %s", exc)
        return {}


_FAQ_DATA = _load_faq_examples()


def _build_faq_text(language: LanguageCode) -> Optional[str]:
    """
    Build a text block with Q&A examples for the prompt.

    Inputs:
        language: Preferred language (es, qu or shp).
    Outputs:
        - String with formatted examples, or None if there is no data.
    """
    lang_data = _FAQ_DATA.get(language) or _FAQ_DATA.get("es")
    if not lang_data:
        return None

    examples = []
    for item in lang_data[:3]:
        q = item.get("question", "").strip()
        a = item.get("answer", "").strip()
        if not q or not a:
            continue
        examples.append(f"- Pregunta: {q}\n  Respuesta: {a}")

    if not examples:
        return None

    return "\n".join(examples)


async def generate_response(
    user_message: str,
    language: LanguageCode,
    alert_hint: bool = False,
    history: Optional[list[dict[str, str]]] = None,
) -> str:
    """
    Generate a Gemini response for a user message.

    Inputs:
        user_message: Current text sent by the person.
        language: Conversation language (es, qu or shp).
        alert_hint: Whether a possible warning sign was detected.
        history: Optional list of previous turns in the conversation
                 with keys `role` ('user' or 'assistant') and `text`.
    Outputs:
        - Text string with the answer in the given language,
          including a short disclaimer at the end.
    """
    faq_text = _build_faq_text(language)
    system_prompt = build_system_prompt(
        language=language,
        alert_hint=alert_hint,
        faq_examples=faq_text,
    )

    history_lines: list[str] = []
    if history:
        # Keep last ~6 messages (about 3 turns) to avoid very long prompts.
        for turn in history[-6:]:
            role = turn.get("role", "user")
            text = (turn.get("text") or "").strip()
            if not text:
                continue
            speaker = "Person" if role == "user" else "Piribot"
            history_lines.append(f"{speaker}: {text}")

    history_block = "\n".join(history_lines)

    if history_block:
        contents = dedent(
            f"""
            {system_prompt}

            Historial breve de la conversación:
            {history_block}

            Mensaje actual de la persona embarazada (idioma: {language}):

            {user_message}
            """
        ).strip()
    else:
        contents = dedent(
            f"""
            {system_prompt}

            Mensaje de la persona embarazada (idioma: {language}):

            {user_message}
            """
        ).strip()

    try:
        # Run the call in a separate thread to avoid blocking the asyncio loop.
        response = await asyncio.to_thread(
            _client.models.generate_content,
            model=_GEMINI_MODEL_NAME,
            contents=contents,
        )

        # In `google-genai`, `response.text` contains the plain text output.
        text = (getattr(response, "text", None) or "").strip()
        if not text:
            raise ValueError("Gemini devolvió una respuesta vacía.")

        # Safety: append a short disclaimer at the end (to avoid overload).
        short_disclaimer = get_short_disclaimer(language)
        if short_disclaimer not in text:
            text = f"{text}\n\n{short_disclaimer}"

        return text

    except Exception as exc:  # pragma: no cover - general error handling
        logger.error("Error generating response with Gemini: %s", exc)
        # Safe default message in case of error
        disclaimer = get_disclaimer(language)
        fallback = (
            "En este momento tengo dificultades técnicas para responder con normalidad. "
            "Aun así, quiero recordarte que tu salud es muy importante.\n\n"
        )
        return fallback + disclaimer


