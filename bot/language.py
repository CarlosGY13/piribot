"""
Language utilities and static messages.

Piribot works in:
- Spanish (es)
- Quechua (qu)
- Shipibo-Konibo (shp)

The Quechua and Shipibo translations are examples and should be reviewed
by native speakers before production use.
"""

from typing import Dict, Literal

from config.settings import LanguageCode

LANG_LABELS: Dict[LanguageCode, str] = {
    "es": "Español",
    "qu": "Quechua",
    "shp": "Shipibo-Konibo",
}

LANG_CODES_BY_LABEL: Dict[str, LanguageCode] = {
    v: k for k, v in LANG_LABELS.items()
}

MessageKey = Literal[
    "welcome",
    "choose_language",
    "language_set",
    "help",
    "disclaimer",
    "short_disclaimer",
    "urgent_alert_prefix",
    "urgent_alert_suffix",
    "fallback_error",
]


MESSAGES: Dict[LanguageCode, Dict[MessageKey, str]] = {
    "es": {
        "welcome": (
            "👋 Hola, soy *Piribot*.\n"
            "Estoy aquí para acompañarte durante tu embarazo con información general y apoyo emocional."
        ),
        "choose_language": (
            "Por favor, elige el idioma en el que prefieres conversar:"
        ),
        "language_set": "Perfecto, conversaremos en Español 🇵🇪.",
        "help": (
            "Puedes escribirme tus dudas o cómo te sientes durante el embarazo y te responderé "
            "con información sencilla y acompañamiento emocional.\n\n"
            "Ejemplos de preguntas:\n"
            "- ¿Es normal sentir náuseas en el primer trimestre?\n"
            "- ¿Qué puedo hacer para dormir mejor?\n"
            "- Me siento preocupada, ¿puedo contarte cómo me siento?"
        ),
        "disclaimer": (
            "⚠️ *Importante*\n"
            "Piribot no reemplaza a una profesional ni a un profesional de salud. "
            "Solo brinda información general y acompañamiento emocional. "
            "Si tienes una urgencia, dolor muy fuerte, sangrado, fiebre o te sientes muy mal, "
            "acude de inmediato al centro de salud u hospital más cercano."
        ),
        "short_disclaimer": (
            "Piribot no reemplaza a una profesional ni a un profesional de salud; "
            "solo brinda información general y acompañamiento emocional."
        ),
        "urgent_alert_prefix": (
            "Lo que cuentas podría ser una *señal de alarma* durante el embarazo."
        ),
        "urgent_alert_suffix": (
            "Te recomiendo que acudas *lo antes posible* a un centro de salud u hospital "
            "y, si es necesario, llames a los servicios de emergencia de tu zona.\n\n"
            "Mientras tanto, trata de no quedarte sola y busca apoyo de alguna persona de confianza."
        ),
        "fallback_error": (
            "Lo siento, en este momento no puedo responder con normalidad.\n"
            "Por favor, intenta nuevamente más tarde. "
            "Si tienes una urgencia, acude al centro de salud u hospital más cercano."
        ),
    },
    "qu": {
        "welcome": (
            "👋 Ñuqaqa *Piribot* kani.\n"
            "Wawawan wañusqa kachkan hampiyta qhawayta munaykichu, "
            "ñuqaqa willayta generalmanta ruwani, mana hamuq doctor nisqaqa kanichu."
        ),
        "choose_language": "Ama hina, ima simipi rimakuyta munankichu, akllay:",
        "language_set": "Allinmi, Quechua simipi rimarisunchis 🇵🇪.",
        "help": (
            "Embrazomanta tapukuyta atinki, ima hina kasqaykita willakuyta atinki, "
            "ñuqaqa kichkakunata y willakuyta aswan simple simipi niyki.\n\n"
            "Tapuykunapaq ñawpaq:\n"
            "- Qallariyniykapi ashnayki normalchu?\n"
            "- Ima ruwaspa allin puñunayta atini?\n"
            "- Manam allinwan kachkani, ¿qa riqsichiyta atinki?"
        ),
        "disclaimer": (
            "⚠️ *Sumaq yuyay*\n"
            "Piribot mana doctor ni enfermera hina kanchu. "
            "General willakuyta sapallan churin, manam diagnósticota churichu. "
            "Sut'iykita, sinchilla nanayta, yawarnillayta, q'omer nanayta utaq "
            "aswan mana allin kasqaykita tiyanqa, "
            "chayqa utaqmi aswan utqaylla hampikamayuq wasiman risqayki."
        ),
        "short_disclaimer": (
            "Piribot mana doctor ni enfermera hina kanchu; "
            "willakuy general sapallan churin."
        ),
        "urgent_alert_prefix": (
            "Rimakuykita uyarispa, embrazopi *peligro* kayta rikuchikuchkan hina."
        ),
        "urgent_alert_suffix": (
            "Ama qhipaman churaychu, utqaylla hampikamayuq wasiman rinayki kallpachakuy.\n\n"
            "Sichus atinki, familia masiykita utaq muyuq runata maqllay, "
            "sapa sapallan kachkuyta ama saqiychu."
        ),
        "fallback_error": (
            "Pampachaway, kunan pacha manam allin kutichiyta atini.\n"
            "Aswanta qhipaman wakmanta q'epiyta yachay. "
            "Sichus aswan sinchi nanay utaq peligro tiyan, utqaylla hampikamayuq wasiman rinayki."
        ),
    },
    "shp": {
        "welcome": (
            "👋 Nete bake, *Piribot* jashiñ.\n"
            "Jakon jaskaraon betea iki shinanti bake yoson jakon maiti, "
            "jaskaraon oraonbo shinanti jaskaraon iikin."
        ),
        "choose_language": "Jenki, jaskaraon iki non iki jain shinanbo, akën:",
        "language_set": "Jakon, Shipibo-Konibo jaisra ikinbo jaskaraon iki 🇵🇪.",
        "help": (
            "Embarazo shinanbo jaskaraon iki, shinanti maiti ikin, "
            "jaskaraon ninkibo non jaskaraon jato jaskatima.\n\n"
            "Jaskaraon tapuesba ainban:\n"
            "- ¿Rari jaskaraon bake embarazobo jawen maiti normal jatonma?\n"
            "- ¿Ja ainban jaton bake wesna bërëman jaskatima?\n"
            "- Jaskaraon pena iki, ¿ja ainbobo ninkibo iki?"
        ),
        "disclaimer": (
            "⚠️ *Jakon jaskaraon*\n"
            "Piribot mana meraya ni doctor jai, ira jaskaraon willaibo jakon oraonbo ani.\n"
            "Non jakon shinanti, jatibi jaskaraon wesna, yawar íbo, "
            "jaskaraon jato wesnati shinanti, jawen nete centro de salud rabi o hospital rabi jakanai."
        ),
        "short_disclaimer": (
            "Piribot mana doctor ni meraya jai; jakon información ja ikinbo "
            "jai onanya jaskaraon."
        ),
        "urgent_alert_prefix": (
            "Jaskaraon ninkibo iki bake embarazobo *peligro* shinanti jakon."
        ),
        "urgent_alert_suffix": (
            "Jawen ja, nete centro de salud rabi o hospital rabi jawe *jaskaraon* jakanai.\n\n"
            "Jaskaraon bake saiyanai ikinma, ja atibobo non familia o amigo shinanti jawe jaskatima."
        ),
        "fallback_error": (
            "Pampachamai, jaskaraon jato nete oraonbo non jaskaraon iki bain.\n"
            "Jatonra iki jaskaraon wesna, nete centro de salud rabi o hospital rabi jakanai."
        ),
    },
}


def get_message(lang: LanguageCode, key: MessageKey) -> str:
    """
    Return a static message for a given language and key.

    If the language does not exist, Spanish is used as default.
    """
    data = MESSAGES.get(lang) or MESSAGES["es"]
    return data[key]


def get_disclaimer(lang: LanguageCode) -> str:
    """
    Shortcut to obtain the full medical disclaimer message.
    """
    return get_message(lang, "disclaimer")


def get_short_disclaimer(lang: LanguageCode) -> str:
    """
    Short disclaimer version to append at the end of responses
    without repeating long texts many times.
    """
    data = MESSAGES.get(lang) or MESSAGES["es"]
    return data["short_disclaimer"]


