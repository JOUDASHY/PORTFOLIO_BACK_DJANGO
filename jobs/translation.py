"""Traduction de texte via Groq (LLM), réutilise la clé déjà configurée.

Appel LLM simple (pas le RAG) : on ne veut qu'une traduction fidèle,
en préservant le HTML léger des descriptions d'offres.
"""
from __future__ import annotations

import logging

from django.conf import settings

logger = logging.getLogger("jobs")

LANG_NAMES = {
    "fr": "français",
    "en": "anglais",
    "es": "espagnol",
    "de": "allemand",
}

# Modèles candidats (ordre de préférence) ; on retombe sur le suivant si l'un
# est décommissionné, comme le fait le RAG existant.
_FALLBACK_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "groq/compound",
]


def _candidate_models() -> list[str]:
    configured = getattr(settings, "GROQ_MODEL", None)
    models = ([configured] if configured else []) + _FALLBACK_MODELS
    return list(dict.fromkeys(models))  # dédoublonne en gardant l'ordre


def translate_text(text: str, target_lang: str = "fr") -> str:
    """Traduit `text` vers `target_lang`. Lève RuntimeError si Groq indisponible."""
    text = (text or "").strip()
    if not text:
        return ""

    api_key = getattr(settings, "GROQ_API_KEY", None)
    if not api_key:
        raise RuntimeError("Clé API Groq non configurée sur le serveur.")

    try:
        from groq import Groq
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("Le paquet 'groq' n'est pas installé.") from exc

    lang_label = LANG_NAMES.get(target_lang, target_lang)
    system_prompt = (
        f"Tu es un traducteur professionnel. Traduis le texte fourni en {lang_label}. "
        "Conserve le sens exact et le ton. Si le texte contient des balises HTML "
        "(p, ul, li, br, strong, a…), garde-les intactes et ne traduis que le texte "
        "visible. Ne rajoute aucun commentaire, renvoie uniquement la traduction."
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": text},
    ]

    client = Groq(api_key=api_key)
    last_error = None
    for model_name in _candidate_models():
        try:
            completion = client.chat.completions.create(
                model=model_name, messages=messages, temperature=0.2
            )
            return completion.choices[0].message.content.strip()
        except Exception as err:  # modèle décommissionné → essayer le suivant
            last_error = err
            msg = str(err)
            if any(k in msg for k in ("model_not_found", "model_decommissioned", "404")):
                continue
            raise
    if last_error:
        raise last_error
    return text
